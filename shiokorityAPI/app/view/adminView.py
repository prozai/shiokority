from flask import Blueprint, request, session, jsonify, send_file
from werkzeug.exceptions import BadRequest
from ..controller.administratorController import AdminController
from ..controller.auditTrailController import AuditTrailController
from ..auth.TOTP import generate_totp_uri, create_qr_code, generate_secret, encrypt_secret, decrypt_secret, get_totp_token

adminBlueprint = Blueprint('adminBlueprint', __name__)

admin_controller = AdminController()
audit_trail_controller = AuditTrailController()

@adminBlueprint.route("/auth/login", methods=['POST'])
def adminLogin():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        email = data.get('email')
        password = data.get('password')

        admin = admin_controller.validate_admin_login(email, password)

        if admin['status']:
            session['loggedIn'] = True
            session['email'] = admin['admin_email']
            audit_trail_controller.log_action('POST', '/admin/auth/login', f"Admin {email} logged in successfully")
            return jsonify(success=True, isMFA=admin['admin_mfa_enabled']), 200
        else:
            audit_trail_controller.log_action('POST', '/admin/auth/login', f"Failed login attempt for {email}")
            return jsonify(success=admin['status'], message=admin['message']), 401

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/auth/login', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/auth/login', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route("/auth/logout", methods=['POST'])
def logout():
    audit_trail_controller.log_action('POST', '/admin/auth/logout', f"Admin {session['email']} logged out")
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant", methods=['POST'])
def createMerchant():

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Failed to create Merchant with data: {data}")
            raise BadRequest("No input data provided")

        createdMerchant = admin_controller.create_merchant(data)

        if createdMerchant:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Merchant created with data: {data}")
            return jsonify(success=True, message='Successfully Created'), 200
        else:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Failed to create Merchant with data: {data}")
            return jsonify(success=False, message="Failed to Created"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('GET', '/admin/view-merchant', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        merchants = admin_controller.get_merchant_data()

        if not merchants:
            audit_trail_controller.log_action('GET', '/admin/view-merchant', "Failed to fetch merchant list")
            return jsonify(success=False, message="No merchants found"), 404
            
        audit_trail_controller.log_action('GET', '/admin/view-merchant', "Viewed merchant list")
        return jsonify(merchants), 200
            
    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/view-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
        
@adminBlueprint.route('/merchants/<merch_id>', methods=['GET'])
def getMerchant(merch_id):

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        merchant = admin_controller.get_one_merchant(merch_id)
        
        if not merchant:
            audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
            return jsonify(success=False, message="Merchant not found"), 404
            
        audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
        return jsonify(merchant), 200

    except Exception as e:
        audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/merchants/<merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        data = request.json
        if not data:
            raise BadRequest("No input data provided")

        updateStatus = admin_controller.update_merchant_details(merch_id, data)

        if not updateStatus:
            audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Updated merchant with data: {data}")
            return jsonify(success=False, message="Failed to update merchant"), 400
        
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Updated merchant with data: {data}")
        return jsonify(success=True), 200

    except BadRequest as e:
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
    
@adminBlueprint.route('/suspend-merchants/<merch_id>', methods=['PUT'])
def updateMerchantStatus(merch_id):

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        data = request.json
        if not data:
            audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Status is missing in the input data")
            raise BadRequest("No input data provided")

        status = data.get('status')
        
        updateStatus = admin_controller.update_merchant_status(merch_id, status)
        
        if not updateStatus:
            audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Failed to update merchant status")
            return jsonify(success=False, message="Failed to update merchant status"), 400
        
        audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', f"Merchant status updated successfully to {status}")
        return jsonify(success=True), 200
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Error updating merchant status " + str(e))
        return jsonify(success=False, message="An unexpected error occurred"), 500


@adminBlueprint.route('/add-user', methods=['POST'])
def addUser():

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('POST', '/admin/add-user', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/admin/add-user', f"Bad Request with data: {data}")
            raise BadRequest("No input data provided")

        createdUser = admin_controller.addUser(data)

        if not createdUser:
            audit_trail_controller.log_action('POST', '/admin/add-user', f"Failed to add user with data: {data}")
            return jsonify(success=False, message="Failed to add user"), 400
        
        audit_trail_controller.log_action('POST', '/admin/add-user', f"User created with data: {data}")
        return jsonify(success=True, message='Successfully Created'), 200
        
    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/add-user', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/add-user', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/get-users', methods=['GET'])
def getAllUser():

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('GET', '/admin/get-users', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        users = admin_controller.get_all_users()

        if not users:
            audit_trail_controller.log_action('GET', '/admin/get-users', "No users found")
            return jsonify({"error": "No users found"}), 404

        audit_trail_controller.log_action('GET', '/admin/get-users', "Retrieved all users")
        return jsonify(users), 200

    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/get-users', f"Unexpected error: {e}")
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"error": "An unexpected error occurred"}), 500

@adminBlueprint.route('/get-user/<int:cust_id>', methods=['GET'])
def getUserById(cust_id):

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        user = admin_controller.get_user_by_id(cust_id)
        
        if not user:
            audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', "User not found")
            return jsonify(success=False, message="User not found"), 404
           
        audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', f"Retrieved user by ID: {cust_id}")
        return jsonify(user), 200
    
    except Exception as e:
        audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', f"Unexpected error: {e}")
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/users/<int:user_id>/update', methods=['PUT'])
def submitUserUpdate(user_id):

    if 'loggedIn' not in session:
        audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', "Unauthorized access")
        return jsonify(success=False, message="Unauthorized access"), 401

    try:
        data = request.get_json()

        if not data:
            audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', "No input data provided")
            raise BadRequest("No input data provided")

        # Extract the necessary fields (similar to addUser)
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        address = data.get('address')
        phone = data.get('phone')
        status = data.get('status')

        updateStatus = admin_controller.submit_user_update(user_id, email, first_name, last_name, address, phone, status)

        if not updateStatus:
            audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', "Failed to update user")
            return jsonify(success=False), 400
        
        audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', f"Updated user details for ID: {user_id}")
        return jsonify(success=True), 200
    
    except Exception as e:
        audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', f"Unexpected error: {e}")
        print(f"Error updating user details: {e}")
        return jsonify({"error": "Failed to update user details"}), 500
    
@adminBlueprint.route('/getQRcode', methods=['GET'])
def getQRcode():
    # need get secret key from database
    user = admin_controller.getAdminTokenByEmail(session['email'])
    
    totp_uri = generate_totp_uri(session['email'], decrypt_secret(user['admin_secret_key']))
    qr_code = create_qr_code(totp_uri)

    audit_trail_controller.log_action('GET', '/admin/getQRcode', f"QR code generated for {session['email']}")
    return send_file(qr_code, mimetype='image/png')
@adminBlueprint.route('/getSecretKey', methods=['GET'])
def getSecretKey():
    user = admin_controller.getAdminTokenByEmail(session['email'])
    de_secret_key = decrypt_secret(user['admin_secret_key'])

    audit_trail_controller.log_action('GET', '/admin/getSecretKey', f"Secret key retrieved for {session['email']}")
    return jsonify(secret_key=de_secret_key)
    
@adminBlueprint.route('/2fa/verify', methods=['POST'])
def verify2FA():
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided')
    
    user = admin_controller.getAdminTokenByEmail(session['email'])
    server_token = get_totp_token(decrypt_secret(user['admin_secret_key']))
    if server_token == data['code']:
        audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"2FA verified for {session['email']}")
        update2FA = admin_controller.update2FAbyEmail(session['email'])
        return jsonify(success=update2FA), 200
    else:
        audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"2FA failed for {session['email']}")
        return jsonify({"error": "Validation Fail"}), 400

# This is the endpoint to get the secret key to insert into the database
@adminBlueprint.route('/get-key', methods=['GET'])
def getKeyToInsert():
    secret_key = encrypt_secret(generate_secret())
    return jsonify(secret_key=secret_key)

@adminBlueprint.route('/getAllAuditTrailLogs', methods=['GET'])
def getAllAuditTrailLogs():
    try:
        logs = audit_trail_controller.get_all_logs()
        if logs:
            audit_trail_controller.log_action('GET', '/admin/getAllAuditTrailLogs', "Retrieved all audit trail logs")
            return jsonify(logs), 200
        else:
            audit_trail_controller.log_action('GET', '/admin/getAllAuditTrailLogs', "No audit trail logs found")
            return jsonify({"message": "No audit trail logs found"}), 404
    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/getAllAuditTrailLogs', f"Unexpected error: {e}")
        print(f"Error retrieving all audit trail logs: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@adminBlueprint.route('/getAuditTrailById/<int:audit_id>', methods=['GET'])
def getAuditTrailById(audit_id):
    try:
        log = audit_trail_controller.get_log_by_id(audit_id)
        if log:
            audit_trail_controller.log_action('GET', f'/admin/getAuditTrailById/{audit_id}', f"Retrieved audit log with ID: {audit_id}")
            return jsonify(log), 200
        else:
            audit_trail_controller.log_action('GET', f'/admin/getAuditTrailById/{audit_id}', f"No audit log found with ID: {audit_id}")
            return jsonify({"message": "Audit trail log not found"}), 404
    except Exception as e:
        audit_trail_controller.log_action('GET', f'/admin/getAuditTrailById/{audit_id}', f"Unexpected error: {e}")
        print(f"Error retrieving audit trail log by ID: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500