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

        email = data.get('email', '')
        password = data.get('password', '')

        if not email or not password:
            raise BadRequest("Email and password are required")

        admin, adminEmail = admin_controller.validate_admin_login(email, password)

        if admin:
            session['loggedIn'] = True
            session['email'] = adminEmail
            audit_trail_controller.log_action('POST', '/admin/auth/login', f"Admin {adminEmail} logged in successfully")
            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('POST', '/admin/auth/login', f"Failed login attempt for {email}")
            return jsonify(success=False, message=adminEmail), 401


    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/auth/login', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/auth/login', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route("/auth/logout", methods=['POST'])
def logout():
    admin_email = session.get('email')
    session.clear()
    audit_trail_controller.log_action('POST', '/admin/auth/logout', f"Admin {admin_email} logged out")
    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant", methods=['POST'])
def createMerchant():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Failed to create Merchant with data: {data}")
            raise BadRequest("No input data provided")

        createdMerchant = admin_controller.create_merchant(data)

        if createdMerchant:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Merchant created with data: {data}")
            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Failed to create Merchant with data: {data}")
            return jsonify(success=False, message="Failed to create merchant"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/create-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = admin_controller.get_merchant_data()

        if merchants:
            audit_trail_controller.log_action('GET', '/admin/view-merchant', "Viewed merchant list")
            return jsonify(merchants), 200
        else:
            audit_trail_controller.log_action('GET', '/admin/view-merchant', "Failed to fetch merchant list")
            return jsonify(success=False, message="No merchants found"), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/view-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
        
@adminBlueprint.route('/merchants/<merch_id>', methods=['GET'])
def getMerchant(merch_id):
    try:
        merchant = admin_controller.get_one_merchant(merch_id)
        
        if merchant:
            audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
            return jsonify(merchant), 200
        else:
            audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
            return jsonify(success=False, message="Merchant not found"), 404

    except Exception as e:
        # print(f"An error occurred: {str(e)}")
        audit_trail_controller.log_action('GET', f'/admin/merchants/{merch_id}', f"Get merchant with data: {merchant}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/merchants/<merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):
    try:
        data = request.json
        if not data:
            raise BadRequest("No input data provided")

        updateStatus = admin_controller.update_merchant_details(merch_id, data)

        if updateStatus:
            audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Updated merchant with data: {data}")
            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Updated merchant with data: {data}")
            return jsonify(success=False, message="Failed to update merchant"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('PUT', f'/admin/merchants/{merch_id}', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
    
@adminBlueprint.route('/suspend-merchants/<merch_id>', methods=['PUT'])
def updateMerchantStatus(merch_id):
    try:
        data = request.json
        if not data:
            audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Status is missing in the input data")
            raise BadRequest("No input data provided")

        status = data.get('status')
        
        updateStatus = admin_controller.update_merchant_status(merch_id, status)
        
        if updateStatus:
            audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', f"Merchant status updated successfully to {status}")
            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Failed to update merchant status")
            return jsonify(success=False, message="Failed to update merchant status"), 400
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        audit_trail_controller.log_action('PUT', f'/admin/suspend-merchants/{merch_id}', "Error updating merchant status " + str(e))
        return jsonify(success=False, message="An unexpected error occurred"), 500


# My work of art
@adminBlueprint.route('/add-user', methods=['POST'])
def addUser():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/admin/add-user', f"Bad Request with data: {data}")
            raise BadRequest("No input data provided")

        createdUser = admin_controller.addUser(data)

        if createdUser:
            audit_trail_controller.log_action('POST', '/admin/add-user', f"User created with data: {data}")
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to add user"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/add-user', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/add-user', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/get-users', methods=['GET'])
def getAllUser():
    try:
        users = admin_controller.get_all_users()
        audit_trail_controller.log_action('GET', '/admin/get-users', "Retrieved all users")

        if users:
            return jsonify(users), 200
        else:
            audit_trail_controller.log_action('GET', '/admin/get-users', "No users found")
            return jsonify({"error": "No users found"}), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/get-users', f"Unexpected error: {e}")
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"error": "An unexpected error occurred"}), 500

@adminBlueprint.route('/get-user/<int:cust_id>', methods=['GET'])
def getUserById(cust_id):
    try:
        user = admin_controller.get_user_by_id(cust_id)
        audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', f"Retrieved user by ID: {cust_id}")

        if user:
            return jsonify(user), 200
        else:
            audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', "User not found")
            return jsonify(success=False, message="User not found"), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', f'/admin/get-user/{cust_id}', f"Unexpected error: {e}")
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/users/<int:user_id>/update', methods=['PUT'])
def submitUserUpdate(user_id):
    try:
        data = request.get_json()

        if not data:
            audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', "No input data provided")
            raise BadRequest("No input data provided")

        # Extract the necessary fields (similar to addUser)
        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        address = data.get('address', None)
        phone = data.get('phone', None)
        status = data.get('status', None)

        updateStatus = admin_controller.submit_user_update(user_id, email, first_name, last_name, address, phone, status)
        audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', f"Updated user details for ID: {user_id}")

        if updateStatus:
            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', "Failed to update user")
            return jsonify(success=False), 400

    except Exception as e:
        audit_trail_controller.log_action('PUT', f'/admin/users/{user_id}/update', f"Unexpected error: {e}")
        print(f"Error updating user details: {e}")
        return jsonify({"error": "Failed to update user details"}), 500
    
@adminBlueprint.route('/getQRcode', methods=['GET'])
def getQRcode():
    try:
        user = admin_controller.getAdminTokenByEmail(session['email'])
        if not user:
            audit_trail_controller.log_action('GET', '/admin/getQRcode', f"Failed to retrieve user for email: {session['email']}")
            return jsonify({"error": "User not found"}), 404

        totp_uri = generate_totp_uri(session['email'], decrypt_secret(user['admin_secret_key']))
        qr_code = create_qr_code(totp_uri)
        audit_trail_controller.log_action('GET', '/admin/getQRcode', f"QR code generated for email: {session['email']}")

        return send_file(qr_code, mimetype='image/png')
    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/getQRcode', f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@adminBlueprint.route('/getSecretKey', methods=['GET'])
def getSecretKey():
    try:
        user = admin_controller.getAdminTokenByEmail(session['email'])
        if not user:
            audit_trail_controller.log_action('GET', '/admin/getSecretKey', f"Failed to retrieve user for email: {session['email']}")
            return jsonify({"error": "User not found"}), 404

        de_secret_key = decrypt_secret(user['admin_secret_key'])
        audit_trail_controller.log_action('GET', '/admin/getSecretKey', f"Retrieved secret key for email: {session['email']}")

        return jsonify(secret_key=de_secret_key)
    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/getSecretKey', f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@adminBlueprint.route('/2fa/verify', methods=['POST'])
def verify2FA():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/admin/2fa/verify', "No data provided")
            raise BadRequest('No data provided')
        
        user = admin_controller.getAdminTokenByEmail(session['email'])
        if not user:
            audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"Failed to retrieve user for email: {session['email']}")
            return jsonify({"error": "User not found"}), 404

        server_token = get_totp_token(decrypt_secret(user['admin_secret_key']))
        if server_token == data['code']:
            update2FA = admin_controller.update2FAbyEmail(session['email'])
            audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"2FA verified for email: {session['email']}")
            return jsonify(success=update2FA), 200
        else:
            audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"2FA verification failed for email: {session['email']}")
            return jsonify({"error": "Invalid code"}), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/admin/2fa/verify', f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@adminBlueprint.route('/getKeyToInsert', methods=['GET'])
def getKeyToInsert():
    try:
        secret_key = encrypt_secret(generate_secret())
        audit_trail_controller.log_action('GET', '/admin/getKeyToInsert', "Generated and encrypted new secret key")
        return jsonify(secret_key=secret_key)
    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/getKeyToInsert', f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500