from flask import Blueprint, request, jsonify, session
from ..controller.merchantController import MerchantController
from ..controller.auditTrailController import AuditTrailController  # Import the AuditTrailController
from ..controller.auditTrailController import AuditTrailController  # Import the AuditTrailController
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity, get_jwt

merchant_instance = MerchantController()
audit_trail_controller = AuditTrailController()

# Create the Blueprint for merchant-related routes
merchantBlueprint = Blueprint('merchant', __name__)

# Route for creating a new merchant (registration)
@merchantBlueprint.route('/register-merchant', methods=['POST'])
def registerMerchant():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/merchant/register-merchant', "No input data provided")
            return jsonify({'success': False, 'message': 'Merchant email, password, first name, last name, phone number, and address are required'}), 400
        
        success, message = merchant_instance.registerMerchant(data)
        
        if success:
            audit_trail_controller.log_action('POST', '/merchant/register-merchant', "Merchant registered successfully")
            return jsonify({'success': True, 'message': message}), 201
        else:
            audit_trail_controller.log_action('POST', '/merchant/register-merchant', f"Merchant registration failed: {message}")
            return jsonify({'success': False, 'message': message}), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/merchant/register-merchant', f"Unexpected error: {e}")
        print(f"Error registering merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during registration'}), 500

# Login Merchant Endpoint
@merchantBlueprint.route('/login', methods=['POST'])
def loginMerchant():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/merchant/login', "Email and password are required")
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        email = data['email']
        password = data['password']

        merchant = merchant_instance.getMerchantByEmail(email)

        if merchant and bcrypt.checkpw(password.encode('utf-8'), merchant['merch_pass'].encode('utf-8')):
            
            access_token = create_access_token(
                identity=email,
                additional_claims={'merch_id':merchant['merch_id']}
            )

            audit_trail_controller.log_action('POST', '/merchant/login', f"Merchant {email} logged in successfully")
            
            return jsonify({
                'success': True, 
                'message': 'Login successful', 
                'merchant': {'merch_id': merchant['merch_id']},
                'access_token': access_token,   
                'refresh_token': create_refresh_token(identity=email)
                }), 200
        else:
            audit_trail_controller.log_action('POST', '/merchant/login', f"Failed login attempt for email: {email}")
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    except Exception as e:
        audit_trail_controller.log_action('POST', '/merchant/login', f"Unexpected error: {e}")
        print(f"Error logging in merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during login'}), 500

# Fetch Merchant Profile Endpoint
@merchantBlueprint.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_identity = get_jwt_identity()
        validateUser = merchant_instance.validateTokenEmail(user_identity)

        if not validateUser:
            audit_trail_controller.log_action('GET', '/merchant/profile', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401
        
        merch_id = get_jwt()['merch_id']

        merchant = merchant_instance.getMerchantByID(merch_id)

        if merchant:
            audit_trail_controller.log_action('GET', '/merchant/profile', f"Retrieved profile for merchant ID {merch_id}")
            return jsonify(merchant), 200
        else:
            audit_trail_controller.log_action('GET', '/merchant/profile', f"Merchant {merch_id} not found")
            return jsonify({'success': False, 'message': 'Merchant not found'}), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/profile', f"Unexpected error: {e}")
        print(f"Error fetching merchant profile: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching the profile'}), 500

# Logout Merchant Endpoint
@merchantBlueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:

        user_identity = get_jwt_identity()
        validateUser = merchant_instance.validateTokenEmail(user_identity)

        if not validateUser:
            audit_trail_controller.log_action('POST', '/merchant/logout', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401
        
        merch_id = get_jwt()['merch_id']

        session.clear()
        audit_trail_controller.log_action('POST', '/merchant/logout', f"Merchant ID {merch_id} logged out successfully")
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        audit_trail_controller.log_action('POST', '/merchant/logout', f"Unexpected error: {e}")
        print(f"Error logging out merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during logout'}), 500

@merchantBlueprint.route('/viewTransactionHistory', methods=['GET'])
@jwt_required()
def viewTransactionHistory():
    try:
        user_identity = get_jwt_identity()
        validateUser = merchant_instance.validateTokenEmail(user_identity)

        if not validateUser:
            audit_trail_controller.log_action('GET', '/merchant/viewTransactionHistory', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401
        
        merch_id = get_jwt()['merch_id']

        transactionHistory = merchant_instance.viewPaymentRecordByMerchId(merch_id)

        if not transactionHistory:
            audit_trail_controller.log_action('GET', '/merchant/viewTransactionHistory', f"No transaction history found for merchant ID {merch_id}")
            return jsonify({'success': False, 'message': 'No transaction history found'}), 404

        audit_trail_controller.log_action('GET', '/merchant/viewTransactionHistory', f"Transaction history retrieved for merchant ID {merch_id}")
        return jsonify(transactionHistory), 200

    except Exception as e:
        audit_trail_controller.log_action('GET', '/merchant/viewTransactionHistory', f"Unexpected error: {e}")
        print(f"Error viewing transaction history: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching transaction history'}), 500