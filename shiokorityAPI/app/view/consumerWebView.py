from flask import Blueprint, request, jsonify, session
from ..models.consumerWeb import consumerWeb
from ..controller.consumerWebController import ConsumerWebController
import bcrypt

consumerWebBlueprint = Blueprint('consumerWeb', __name__)
consumerWeb_instance = consumerWeb()

@consumerWebBlueprint.route('/register-consumerWeb', methods=['POST'])
def registerConsumer():
    data = request.get_json()

    # Extract data from request
    cust_email = data.get('cust_email')
    cust_pass = data.get('password') # Plain-text password entered by the user
    cust_name = data.get('cust_name')
    cust_phone = data.get('cust_phone')
    cust_address = data.get('cust_address')

    success, message = consumerWeb_instance.registerConsumer(cust_email, cust_pass, cust_name, cust_phone, cust_address)
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'message': message}), 400

@consumerWebBlueprint.route('/login-consumer', methods=['POST'])
def loginConsumer():
    data = request.get_json()

    email = data['email']
    password = data['password'] # Plain-text password entered by the user

    # Fetch the consumer from the database
    consumer = consumerWeb_instance.getConsumerByEmail(email)

    # Verify the password using native bcrypt
    if consumer and bcrypt.checkpw(password.encode('utf-8'), consumer['cust_pass'].encode('utf-8')):
        # Store the consumer ID in the session upon successful login
        session['cust_id'] = consumer['cust_id']
        return jsonify({'success': True, 'message': 'Login successful', 'customer': {'cust_id': consumer['cust_id']}}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401


# Fetch Consumer Profile Endpoint
@consumerWebBlueprint.route('/profile', methods=['GET'])
def profile():
    if 'cust_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

    consumer = consumerWeb_instance.getConsumerByID(session['cust_id'])

    if consumer:
        return jsonify(consumer), 200
    else:
        return jsonify({'success': False, 'message': 'Consumer not found'}), 404
    

@consumerWebBlueprint.route('/send-transaction', methods=['POST'])
def sendTransaction():
    data = request.get_json()

    consumer_email = data.get('consumer_email')
    merch_email = data.get('merch_email')
    amount = data.get('amount')

    if not consumer_email or not merch_email or not amount:
        return jsonify({'success': False, 'message': 'Consumer email, merchant email, and amount are required'}), 400

    success, message = ConsumerWebController.sendTransaction(consumer_email, merch_email, amount)

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400