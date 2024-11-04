from flask import Blueprint, request, jsonify, session
from werkzeug.exceptions import BadRequest
from ..controller.consumerController import ConsumerController
from ..controller.auditTrailController import AuditTrailController  # Added by lu
import bcrypt
from ..models.fraudDetection import FraudDetection

consumerBlueprint = Blueprint('consumerBlueprint', __name__)
consumer_instance = ConsumerController()
audit_trail_controller = AuditTrailController()

@consumerBlueprint.route('/register-consumer', methods=['POST'])
def registerConsumer():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', 'consu/register-consumer', "No input data provided")
            return jsonify({'success': False, 'message': 'Consumer email, password, first name, last name, phone number, and address are required'}), 400

        success, message = consumer_instance.registerConsumer(data)
        audit_trail_controller.log_action('POST', '/register-consumer', f"Consumer registration {'successful' if success else 'failed'}: {message}")
        
        if success:
            return jsonify({'success': True, 'message': message}), 201
        else:
            return jsonify({'success': False, 'message': message}), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/register-consumer', f"Unexpected error: {e}")
        print(f"Error registering consumer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during registration'}), 500

@consumerBlueprint.route('/login-consumer', methods=['POST'])
def loginConsumer():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            audit_trail_controller.log_action('POST', '/login-consumer', "Email and password are required")
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        email = data['email']
        password = data['password']

        consumer = consumer_instance.getConsumerByEmail(email)
        
        if consumer and bcrypt.checkpw(password.encode('utf-8'), consumer['cust_pass'].encode('utf-8')):
            session['cust_id'] = consumer['cust_id']
            audit_trail_controller.log_action('POST', '/login-consumer', f"Consumer {email} logged in successfully")
            return jsonify({'success': True, 'message': 'Login successful', 'customer': {'cust_id': consumer['cust_id']}}), 200
        else:
            audit_trail_controller.log_action('POST', '/login-consumer', f"Failed login attempt for email: {email}")
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    except Exception as e:
        audit_trail_controller.log_action('POST', '/login-consumer', f"Unexpected error: {e}")
        print(f"Error logging in consumer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during login'}), 500

@consumerBlueprint.route('/logout-consumer', methods=['POST'])
def logoutConsumer():
    try:
        cust_id = session.get('cust_id')
        session.clear()
        audit_trail_controller.log_action('POST', '/logout-consumer', f"Consumer ID {cust_id} logged out")
        return jsonify({'success': True, 'message': 'Logout successful'}), 200
    except Exception as e:
        audit_trail_controller.log_action('POST', '/logout-consumer', f"Unexpected error: {e}")
        print(f"Error logging out consumer: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during logout'}), 500

@consumerBlueprint.route('/profile-consumer', methods=['GET'])
def profile():
    try:
        if 'cust_id' not in session:
            audit_trail_controller.log_action('GET', '/profile-consumer', "Unauthorized access attempt")
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

        consumer = consumer_instance.getConsumerByID(session['cust_id'])
        
        if consumer:
            audit_trail_controller.log_action('GET', '/profile-consumer', f"Profile retrieved for consumer ID {session['cust_id']}")
            return jsonify(consumer), 200
        else:
            audit_trail_controller.log_action('GET', '/profile-consumer', f"Consumer ID {session['cust_id']} not found")
            return jsonify({'success': False, 'message': 'Consumer not found'}), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/profile-consumer', f"Unexpected error: {e}")
        print(f"Error fetching consumer profile: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred while fetching the profile'}), 500

@consumerBlueprint.route('/send-payment', methods=['POST'])
def sendPayment():
    try:
        data = request.get_json()
        if not data:
            audit_trail_controller.log_action('POST', '/send-payment', "Missing payment data")
            return jsonify({'success': False, 'message': 'Missing Value'}), 400

        # Validate UEN
        if not consumer_instance.validateUEN(data['uen']):
            audit_trail_controller.log_action('POST', '/send-payment', f"Invalid UEN: {data['uen']}")
            return jsonify({'success': False, 'message': 'Invalid UEN'}), 400

        # Validate card
        success, message = consumer_instance.customerValidateCardProcedure(data['cardNumber'], data['cvv'], data['expiryDate'])
        
        if not success:
            audit_trail_controller.log_action('POST', '/send-payment', f"Card validation failed: {message}")
            return jsonify({'success': False, 'message': message}), 400

        # Process payment
        success, message = consumer_instance.processPaymentProcedure(data)
        audit_trail_controller.log_action('POST', '/send-payment', f"Payment processing {'successful' if success else 'failed'}: {message}")
        
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'message': message}), 400

    except Exception as e:
        audit_trail_controller.log_action('POST', '/send-payment', f"Unexpected error: {e}")
        print(f"Error processing payment: {e}")
        return jsonify({'success': False, 'message': 'An unexpected error occurred during payment processing'}), 500

@consumerBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = consumer_instance.get_merchant_data()
        if merchants:
            audit_trail_controller.log_action('GET', '/view-merchant', "Merchant list viewed successfully")
            return jsonify(merchants), 200
        else:
            audit_trail_controller.log_action('GET', '/view-merchant', "No merchants found")
            return jsonify({'success': False, 'message': "No merchants found"}), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/view-merchant', f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': "An unexpected error occurred"}), 500