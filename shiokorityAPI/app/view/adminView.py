from flask import Blueprint, request, session, jsonify, send_file
from werkzeug.exceptions import BadRequest
from ..controller.administratorController import AdminController
from ..controller.auditTrailController import AuditTrailController  # Import the AuditTrailController
from ..auth.TOTP import generate_totp_uri, create_qr_code, generate_secret, encrypt_secret, decrypt_secret, get_totp_token

adminBlueprint = Blueprint('adminBlueprint', __name__)

admin_controller = AdminController()
audit_trail_controller = AuditTrailController()  # Create an instance of the AuditTrailController

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

            # Log the login action
            audit_trail_controller.log_action('POST', '/auth/login', f"Admin {adminEmail} logged in successfully")

            return jsonify(success=True), 200
        else:
            audit_trail_controller.log_action('POST', '/auth/login', f"Failed login attempt for {email}")
            return jsonify(success=False), 401

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/auth/login', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/auth/login', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route("/auth/logout", methods=['POST'])
def logout():
    admin_email = session.get('email')
    session.clear()

    # Log the logout action
    audit_trail_controller.log_action('POST', '/auth/logout', f"Admin {admin_email} logged out")

    return jsonify({'message': 'Logout successful'}), 200

@adminBlueprint.route("/create-merchant", methods=['POST'])
def createMerchant():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        createdMerchant = admin_controller.create_merchant(data)

        # Log the merchant creation action
        audit_trail_controller.log_action('POST', '/create-merchant', f"Merchant created with data: {data}")

        if createdMerchant:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to create merchant"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/create-merchant', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/create-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = admin_controller.get_merchant_data()

        # Log the action of viewing merchants
        audit_trail_controller.log_action('GET', '/view-merchant', "Viewed merchant list")

        if merchants:
            return jsonify(merchants), 200
        else:
            return jsonify(success=False, message="No merchants found"), 404
            
    except Exception as e:
        audit_trail_controller.log_action('GET', '/view-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/merchants/<merch_id>', methods=['PUT'])
def submitMerchantUpdate(merch_id):
    try:
        data = request.json

        if not data:
            raise BadRequest("No input data provided")

        updateStatus = admin_controller.update_merchant_details(merch_id, data)

        # Log the merchant update action
        audit_trail_controller.log_action('PUT', f'/merchants/{merch_id}', f"Updated merchant with data: {data}")

        if updateStatus:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to update merchant"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('PUT', f'/merchants/{merch_id}', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('PUT', f'/merchants/{merch_id}', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

@adminBlueprint.route('/add-user', methods=['POST'])
def addUser():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        createdUser = admin_controller.addUser(data)

        # Log the user creation action
        audit_trail_controller.log_action('POST', '/add-user', f"User created with data: {data}")

        if createdUser:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Failed to add user"), 400

    except BadRequest as e:
        audit_trail_controller.log_action('POST', '/add-user', f"Error: {str(e)}")
        return jsonify(success=False, message=str(e)), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/add-user', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

# Continue updating other endpoints similarly...
