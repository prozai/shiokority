# app/controller/merchantController.py
from flask import Blueprint, request, jsonify, session
from ..controller.merchantController import MerchantController
import bcrypt
from ..controller.auditTrailController import AuditTrailController 

merchant_instance = MerchantController()
audit_trail_controller = AuditTrailController()

# Create the Blueprint for merchant-related routes
merchantBlueprint = Blueprint('merchant', __name__)


# Route for creating a new merchant (registration)
@merchantBlueprint.route('/register-merchant', methods=['POST'])
def registerMerchant():
    # data include merch_name, merch_email, merch_pass, merch_phone, merch_address, uen
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Merchant email, password, first name, last name, phone number, and address are required'}), 400
    
    # Call the Merchant model to create the new merchant
    success, message = merchant_instance.registerMerchant(data)
    
    if success:
        audit_trail_controller.log_action('POST', '/register-merchant', f"Registered merchant with email {data['email']}")
        return jsonify({'success': True, 'message': message}), 201  # 201 = Created
    else:
        audit_trail_controller.log_action('POST', '/register-merchant', f"Failed to register merchant with email {data['email']}")
        return jsonify({'success': False, 'message': message}), 400  # 400 = Bad Request


# Login Merchant Endpoint
@merchantBlueprint.route('/login', methods=['POST'])
def loginMerchant():
    data = request.get_json()

    email = data['email']
    password = data['password'] # Plain-text password entered by the user

    # Fetch the merchant from the database
    merchant = merchant_instance.getMerchantByEmail(email)

    # Verify the password using native bcrypt
    # The plain-text password (password) is compared with the hashed password (merchant['pass_hash'])
    if merchant and bcrypt.checkpw(password.encode('utf-8'), merchant['merch_pass'].encode('utf-8')):
        # Store the merchant ID in the session upon successful login
        session['merch_id'] = merchant['merch_id']
        audit_trail_controller.log_action('POST', '/login', f"Logged in merchant with email {email}")
        return jsonify({'success': True, 'message': 'Login successful', 'merchant': {'merch_id': merchant['merch_id']}}), 200
    else:
        audit_trail_controller.log_action('POST', '/login', f"Failed to log in merchant with email {email}")
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401


# Fetch Merchant Profile Endpoint
@merchantBlueprint.route('/profile', methods=['GET'])
def profile():
    if 'merch_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

    # Fetch the merchant profile
    merchant = merchant_instance.getMerchantByID(session['merch_id'])

    if merchant:    
        audit_trail_controller.log_action('GET', '/profile', f"Viewed profile of merchant with ID {session['merch_id']}")
        return jsonify(merchant), 200
    else:
        audit_trail_controller.log_action('GET', '/profile', f"Failed to view profile of merchant with ID {session['merch_id']}")
        return jsonify({'success': False, 'message': 'Merchant not found'}), 404

# Logout Merchant Endpoint
@merchantBlueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@merchantBlueprint.route('/viewTransactionHistory', methods=['GET'])
def viewTransactionHistory():

    if 'merch_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

    
    transactionHistory = merchant_instance.viewPaymentRecordByMerchId(session['merch_id'])

    if not transactionHistory:
        audit_trail_controller.log_action('GET', '/viewTransactionHistory', f"Failed to view transaction history of merchant with ID {session['merch_id']}")
        return jsonify({'success': False, 'message': 'No transaction history found'}), 404

    audit_trail_controller.log_action('GET', '/viewTransactionHistory', f"Viewed transaction history of merchant with ID {session['merch_id']}")
    return jsonify(transactionHistory), 200