from flask import Blueprint, request, jsonify, session
from werkzeug.exceptions import BadRequest
from ..controller.consumerController import ConsumerController
import bcrypt

consumerBlueprint = Blueprint('consumerBlueprint', __name__)
consumer_instance = ConsumerController()

# @consumerBlueprint.route('/consumer/process-payment', methods=['POST'])
# def processPayment():
#     try:
#         data = request.get_json()

#         merchant_id = data.get('merch_id')
#         amount = data.get('amount')
        
#         if merchant_id is None or amount is None:
#             raise BadRequest("Merchant ID and amount are required")
        
#         checkMerchant = ConsumerController().validateMerchant(merchant_id)

#         if not checkMerchant:
#             return jsonify(success=False, message="Merchant not found or not valid")
    
#         paymentStatus = ConsumerController().process_payment(merchant_id, amount)

#         return jsonify(paymentStatus)

#     except BadRequest as e:
#         return jsonify(success=False, message=str(e)), 400
    
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return jsonify(success=False, message="An unexpected error occurred"), 500
    
@consumerBlueprint.route('/register-consumer', methods=['POST'])
def registerConsumer():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Consumer email, password, first name, last name, phone number, and address are required'}), 400

    success, message = consumer_instance.registerConsumer(data)
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
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
        return jsonify({'success': True, 'message': 'Login successful', 'customer': {'cust_id': consumer['cust_id']}}), 200
    else:
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
        return jsonify(consumer), 200
    else:
        return jsonify({'success': False, 'message': 'Consumer not found'}), 404
    

@consumerBlueprint.route('/send-payment', methods=['POST'])
def sendPayment():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Missing Value'}), 400
    
    # data consists of the following keys: cust_email, merch_email, amount, cardNumber, expiryDate, cvv

    # 0. Need to tokenize the card number and pass it to the bank in the model not here
    # 1. Validate the card (need to tokenize the card number and pass it to the bank)
    # 2. if the card is valid, process the payment

    # validate the card
    success, message = ConsumerController().customerValidateCardProcedure(data['cardNumber'], data['cvv'], data['expiryDate'])

    # if the card is invalid, return the error message
    if not success:
        return jsonify({'success': False, 'message': message}), 400
    
    # if the card is valid, process the payment
    success, message = consumer_instance.processPayment(data)

    if success:
        return jsonify({'success': True, 'message':message}), 200
    else:
        return jsonify({'success': False, 'message':message}), 400