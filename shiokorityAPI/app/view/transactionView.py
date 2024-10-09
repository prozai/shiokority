from flask import Blueprint, request, jsonify
from ..controller.transactionController import TransactionController

transactionBlueprint = Blueprint('transaction', __name__)
transaction_controller = TransactionController()

@transactionBlueprint.route('/add-transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    success, message = transaction_controller.add_transaction(data)
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'message': message}), 400

@transactionBlueprint.route('/transaction-history', methods=['GET'])
def transaction_history():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'success': False, 'message': 'Customer ID is required'}), 400
    
    transactions, balance = transaction_controller.get_transaction_history(customer_id)
    if transactions is not None:
        return jsonify({'success': True, 'transactions': transactions, 'balance': balance}), 200
    else:
        return jsonify({'success': False, 'message': 'No transactions found'}), 404

@transactionBlueprint.route('/update-transaction-status', methods=['PUT'])
def update_transaction_status():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    transaction_id = data.get('transaction_id')
    status = data.get('status')

    if not transaction_id or not status:
        return jsonify({'success': False, 'message': 'Transaction ID and status are required'}), 400
    
    success, message = transaction_controller.update_transaction_status(transaction_id, status)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400