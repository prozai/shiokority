from flask import Blueprint, request, jsonify, session
from ..controller.merchantController import MerchantController
from ..controller.auditTrailController import AuditTrailController  # Import the AuditTrailController
import bcrypt

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
            audit_trail_controller.log_action('POST', '/register-merchant', "No input data provided")
            return jsonify({'success': False, 'message': 'Merchant email, password, first name, last name, phone number, and address are required'}), 400
        
        success, message = merchant_instance.registerMerchant(data)
        
        if success:
            audit_trail_controller.log_action('POST', '/register-merchant', "Merchant registered successfully")
            return jsonify({'success': True, 'message': message}), 201
        else:
            audit_trail_controller.log_action('POST', '/register-merchant', f"Merchant registration failed: {message}")
            return jsonify({'success': False, 'message': message}), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/register-merchant', f"Unexpected error: {e}")
        print(f"Error registering merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during registration'}), 500

# Login Merchant Endpoint
@merchantBlueprint.route('/login', methods=['POST'])
def loginMerchant():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            audit_trail_controller.log_action('POST', '/login', "Email and password are required")
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        email = data['email']
        password = data['password']

        merchant = merchant_instance.getMerchantByEmail(email)

        if merchant and bcrypt.checkpw(password.encode('utf-8'), merchant['merch_pass'].encode('utf-8')):
            session['merch_id'] = merchant['merch_id']
            audit_trail_controller.log_action('POST', '/login', f"Merchant {email} logged in successfully")
            return jsonify({'success': True, 'message': 'Login successful', 'merchant': {'merch_id': merchant['merch_id']}}), 200
        else:
            audit_trail_controller.log_action('POST', '/login', f"Failed login attempt for email: {email}")
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    except Exception as e:
        audit_trail_controller.log_action('POST', '/login', f"Unexpected error: {e}")
        print(f"Error logging in merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during login'}), 500

# Fetch Merchant Profile Endpoint
@merchantBlueprint.route('/profile', methods=['GET'])
def profile():
    try:
        if 'merch_id' not in session:
            audit_trail_controller.log_action('GET', '/profile', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        merchant = merchant_instance.getMerchantByID(session['merch_id'])

        if merchant:
            audit_trail_controller.log_action('GET', '/profile', f"Retrieved profile for merchant ID {session['merch_id']}")
            return jsonify(merchant), 200
        else:
            audit_trail_controller.log_action('GET', '/profile', f"Merchant ID {session['merch_id']} not found")
            return jsonify({'success': False, 'message': 'Merchant not found'}), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/profile', f"Unexpected error: {e}")
        print(f"Error fetching merchant profile: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching the profile'}), 500

# Logout Merchant Endpoint
@merchantBlueprint.route('/logout', methods=['POST'])
def logout():
    try:
        merch_id = session.get('merch_id')
        session.clear()
        audit_trail_controller.log_action('POST', '/logout', f"Merchant ID {merch_id} logged out successfully")
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        audit_trail_controller.log_action('POST', '/logout', f"Unexpected error: {e}")
        print(f"Error logging out merchant: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during logout'}), 500

@merchantBlueprint.route('/viewTransactionHistory', methods=['GET'])
def viewTransactionHistory():
    try:
        if 'merch_id' not in session:
            audit_trail_controller.log_action('GET', '/viewTransactionHistory', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        transactionHistory = merchant_instance.viewPaymentRecordByMerchId(session['merch_id'])

        if not transactionHistory:
            audit_trail_controller.log_action('GET', '/viewTransactionHistory', f"No transaction history found for merchant ID {session['merch_id']}")
            return jsonify({'success': False, 'message': 'No transaction history found'}), 404

        audit_trail_controller.log_action('GET', '/viewTransactionHistory', f"Transaction history retrieved for merchant ID {session['merch_id']}")
        return jsonify(transactionHistory), 200

    except Exception as e:
        audit_trail_controller.log_action('GET', '/viewTransactionHistory', f"Unexpected error: {e}")
        print(f"Error viewing transaction history: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching transaction history'}), 500
