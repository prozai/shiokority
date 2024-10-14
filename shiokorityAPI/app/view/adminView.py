from flask import Blueprint, request, session, jsonify, send_file
from werkzeug.exceptions import BadRequest
from ..controller.administratorController import AdminController
from ..auth.TOTP import generate_totp_uri, create_qr_code, generate_secret, encrypt_secret, decrypt_secret, get_totp_token

adminBlueprint = Blueprint('adminBlueprint', __name__)

admin_controller = AdminController()

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

        admin = admin_controller.validate_admin_login(email, password)
        
        if admin:
            session['loggedIn'] = True
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 401

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route("/auth/logout", methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant", methods=['POST'])
def createMerchant():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        createdMerchant = admin_controller.create_merchant(data)

        if createdMerchant:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to create merchant"), 400

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = admin_controller.get_merchant_data()
        if merchants:
            return jsonify(merchants), 200
        else:
            return jsonify(success=False, message="No merchants found"), 404
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
        
@adminBlueprint.route('/merchants/<merch_id>', methods=['GET'])
def getMerchant(merch_id):
    try:
        merchant = admin_controller.get_one_merchant(merch_id)
        
        if merchant:
            return jsonify(merchant), 200
        else:
            return jsonify(success=False, message="Merchant not found"), 404

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/merchants/<merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):
    try:
        data = request.json

        if not data:
            raise BadRequest("No input data provided")

        updateStatus = admin_controller.update_merchant_details(merch_id, data)
        
        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to update merchant"), 400
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
    
@adminBlueprint.route('/suspend-merchants/<merch_id>', methods=['PUT'])
def updateMerchantStatus(merch_id):
    try:
        data = request.json
        if not data:
            raise BadRequest("No input data provided")

        status = data.get('status')
        
        updateStatus = admin_controller.update_merchant_status(merch_id, status)
        
        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to update merchant status"), 400
        
    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500


# My work of art
@adminBlueprint.route("/add-user", methods=['POST'])
def addUser():
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request

        if not data:
            raise BadRequest("No input data provided")

        createdUser = admin_controller.addUser(data)

        if createdUser:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 400



@adminBlueprint.route('/get-users', methods=['GET'])
def getAllUser():
    try:
        users = admin_controller.get_all_users()
        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": "No users found"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"error": "An unexpected error occurred"}), 500

@adminBlueprint.route('/get-user/<string:cust_id>', methods=['GET'])
def getUserById(cust_id):
    try:
        user = admin_controller.get_user_by_id(cust_id)  # Assuming you have this method in your controller

        if user:
            return jsonify(user), 200
        else:
            return jsonify(success=False, message="User not found"), 404

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500


@adminBlueprint.route('/users/<string:user_id>/update', methods=['PUT'])
def submitUserUpdate(user_id):
    try:
        data = request.get_json()

        # Extract the necessary fields (similar to addUser)
        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        address = data.get('address', None)
        phone = data.get('phone', None)
        status = data.get('status', None)

        # Update the user with the new details
        updateStatus = admin_controller.submit_user_update(user_id, email, first_name, last_name, address, phone, status)

        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False), 400

    except Exception as e:
        print(f"Error updating user details: {e}")
        return jsonify({"error": "Failed to update user details"}), 500
    
@adminBlueprint.route('/getQRcode', methods=['GET'])
def getQRcode():
    
    # need get secret key from database
    user = admin_controller.getAdminTokenByEmail(session['email'])
    
    totp_uri = generate_totp_uri(session['email'], decrypt_secret(user['admin_secret_key']))
    qr_code = create_qr_code(totp_uri)
    
    return send_file(qr_code, mimetype='image/png')
@adminBlueprint.route('/getSecretKey', methods=['GET'])
def getSecretKey():
    user = admin_controller.getAdminTokenByEmail(session['email'])
    de_secret_key = decrypt_secret(user['admin_secret_key'])
    return jsonify(secret_key=de_secret_key)
    
@adminBlueprint.route('/2fa/verify', methods=['POST'])
def verify2FA():
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided')
    
    user = admin_controller.getAdminTokenByEmail(session['email'])
    server_token = get_totp_token(decrypt_secret(user['admin_secret_key']))
    if server_token == data['code']:
        update2FA = admin_controller.update2FAbyEmail(session['email'])
        return jsonify(success=update2FA), 200
    else:
        return jsonify({"error": "Failed to update user details"}), 400