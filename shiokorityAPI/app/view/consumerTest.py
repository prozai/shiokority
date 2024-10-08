from flask import Blueprint, request, jsonify
from ..controller.consumerController import ConsumerController

consumerBlueprint = Blueprint('consumer', __name__)
consumer_controller = ConsumerController()

@consumerBlueprint.route('/register-consumer', methods=['POST'])
def register_consumer():
    data = request.get_json()

    if not data.get('name') or not data.get('email'):
        return jsonify({'success': False, 'message': 'Name and email are required'}), 400

    success, message = consumer_controller.register_consumer(data)
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'message': message}), 400

@consumerBlueprint.route('/send-transaction', methods=['POST'])
def send_transaction():
    data = request.get_json()

    consumer_email = data.get('consumer_email')
    merch_email = data.get('merch_email')
    amount = data.get('amount')

    if not consumer_email or not merch_email or not amount:
        return jsonify({'success': False, 'message': 'Consumer email, merchant email, and amount are required'}), 400

    success, message = consumer_controller.send_transaction(consumer_email, merch_email, amount)

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400