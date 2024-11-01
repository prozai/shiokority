from flask import Blueprint, request, jsonify, session
from werkzeug.exceptions import BadRequest
from ..controller.consumerController import ConsumerController
from ..controller.auditTrailController import AuditTrailController #Added by lu
import bcrypt
from ..models.fraudDetection import FraudDetection


consumerBlueprint = Blueprint('consumerBlueprint', __name__)
consumer_instance = ConsumerController()
audit_trail_controller = AuditTrailController()
    
@consumerBlueprint.route('/register-consumer', methods=['POST'])
def registerConsumer():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Consumer email, password, first name, last name, phone number, and address are required'}), 400

    success, message = consumer_instance.registerConsumer(data)
    
    if success:
        audit_trail_controller.log_action('POST', '/register-consumer', f"Registered consumer with email {data['email']}")
        return jsonify({'success': True, 'message': message}), 201
    else:
        audit_trail_controller.log_action('POST', '/register-consumer', f"Failed to register consumer with email {data['email']}")
        return jsonify({'success': False, 'message': message}), 400

@consumerBlueprint.route('/login-consumer', methods=['POST'])
def loginConsumer():
    data = request.get_json()

    email = data['email']
    password = data['password'] # Plain-text password entered by the user

    # Fetch the consumer from the database
    consumer = consumer_instance.getConsumerByEmail(email)
    
    # Verify the password using native bcrypt
    if consumer and bcrypt.checkpw(password.encode('utf-8'), consumer['cust_pass'].encode('utf-8')):
        # Store the consumer ID in the session upon successful login
        session['cust_id'] = consumer['cust_id']

        audit_trail_controller.log_action('POST', '/login-consumer', f"Logged in consumer with email {email}")
        return jsonify({'success': True, 'message': 'Login successful', 'customer': {'cust_id': consumer['cust_id']}}), 200
    else:
        audit_trail_controller.log_action('POST', '/login-consumer', f"Failed to log in consumer with email {email}")
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@consumerBlueprint.route('/logout-consumer', methods=['POST'])
def logoutConsumer():
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'}), 200

# Fetch Consumer Profile Endpoint
@consumerBlueprint.route('/profile-consumer', methods=['GET'])
def profile():
    if 'cust_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

    consumer = consumer_instance.getConsumerByID(session['cust_id'])
    
    if consumer:
        audit_trail_controller.log_action('GET', '/profile-consumer', f"Viewed profile of consumer with ID {session['cust_id']}")
        return jsonify(consumer), 200
    else:
        audit_trail_controller.log_action('GET', '/profile-consumer', f"Failed to fetch profile of consumer with ID {session['cust_id']}")
        return jsonify({'success': False, 'message': 'Consumer not found'}), 404
    

@consumerBlueprint.route('/send-payment', methods=['POST'])
def sendPayment():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'Missing Value'}), 400
    
    # data consists of the following keys: cust_email, merch_email, amount, cardNumber, expiryDate, cvv, uen

    # validate UEN
    success = ConsumerController().validateUEN(data['uen'])

    if not success:
        audit_trail_controller.log_action('POST', '/send-payment', f"Invalid UEN {data['uen']}")
        return jsonify({'success': False, 'message': 'Invalid UEN'}), 400

    # 0. Need to tokenize the card number and pass it to the bank in the model 
    # 1. Validate the card (need to tokenize the card number and pass it to the bank)
    # 2. if the card is valid, process the payment

    # validate the card (need to do tokenization)
    success, message = ConsumerController().customerValidateCardProcedure(data['cardNumber'], data['cvv'], data['expiryDate'])

    # if the card is invalid, return the error message
    if not success:
        audit_trail_controller.log_action('POST', '/send-payment', f"Incorrect card details for consumer with email {data['cust_email']}")
        return jsonify({'success': False, 'message': message}), 400
    
    # if the card is valid, process the payment
    success, message = ConsumerController().processPaymentProcedure(data)
    
    if success:
        audit_trail_controller.log_action('POST', '/send-payment', f"Payment sent by consumer with email {data['cust_email']} to merchant with UEN {data['uen']}")
        return jsonify({'success': True, 'message':message}), 200
    else:
        audit_trail_controller.log_action('POST', '/send-payment', f"Failed to send payment by consumer with email {data['cust_email']} to merchant with UEN {data['uen']}")
        return jsonify({'success': False, 'message':message}), 400
    

#Added by lu
@consumerBlueprint.route('/view-merchant', methods=['GET'])
def fetchMerchantList():
    try:
        merchants = ConsumerController().get_merchant_data()

        if merchants:
            audit_trail_controller.log_action('GET', '/admin/view-merchant', "Viewed merchant list")
            return jsonify(merchants), 200
        else:
            audit_trail_controller.log_action('GET', '/admin/view-merchant', "Failed to fetch merchant list")
            return jsonify(success=False, message="No merchants found"), 404

    except Exception as e:
        audit_trail_controller.log_action('GET', '/admin/view-merchant', f"Unexpected error: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500
