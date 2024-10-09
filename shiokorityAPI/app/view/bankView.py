from flask import Blueprint, request, jsonify
from ..controller.bankController import BankController

bankBlueprint = Blueprint('bank', __name__)
bank_controller = BankController()

@bankBlueprint.route('/process-transaction', methods=['POST'])
def process_transaction():
    data = request.get_json()
    consumer_email = data.get('consumer_email')
    merch_email = data.get('merch_email')
    amount = data.get('amount')

    if not consumer_email or not merch_email or not amount:
        return jsonify({'success': False, 'message': 'Consumer email, merchant email, and amount are required'}), 400

    success, message = bank_controller.process_transaction(consumer_email, merch_email, amount)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400

@bankBlueprint.route('/refund-transaction', methods=['POST'])
def refund_transaction():
    data = request.get_json()
    payment_id = data.get('payment_id')
    amount = data.get('amount')
    merch_id = data.get('merch_id')

    if not payment_id or not amount or not merch_id:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    success, message = bank_controller.refund_transaction(payment_id, amount, merch_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400

@bankBlueprint.route('/merchant-balance', methods=['GET'])
def get_merchant_balance():
    merch_id = request.args.get('merch_id')

    if not merch_id:
        return jsonify({'success': False, 'message': 'Merchant ID is required'}), 400

    balance = bank_controller.get_merchant_balance(merch_id)

    if balance is not None:
        return jsonify({'success': True, 'balance': balance}), 200
    else:
        return jsonify({'success': False, 'message': 'Merchant not found'}), 404


