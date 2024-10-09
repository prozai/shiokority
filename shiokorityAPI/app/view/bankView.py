from flask import Blueprint, request, jsonify
from ..controller.bankController import BankController
from werkzeug.exceptions import BadRequest

bankBlueprint = Blueprint('bankBlueprint', __name__)
bank_controller = BankController()

# Process a transaction between consumer and merchant
@bankBlueprint.route('/process-transaction', methods=['POST'])
def process_transaction():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        consumer_id = data.get('consumer_id')
        merchant_id = data.get('merchant_id')
        amount = data.get('amount')

        if not consumer_id or not merchant_id or not amount:
            raise BadRequest("Consumer ID, Merchant ID, and amount are required")

        success, message = bank_controller.process_transaction(consumer_id, merchant_id, amount)

        if success:
            return jsonify(success=True, message=message), 200
        else:
            return jsonify(success=False, message=message), 400

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500

# Process a refund for a specific transaction
@bankBlueprint.route('/refund', methods=['POST'])
def refund_transaction():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No input data provided")

        transaction_id = data.get('transaction_id')
        amount = data.get('amount')

        if not transaction_id or not amount:
            raise BadRequest("Transaction ID and amount are required")

        success, message = bank_controller.refund_transaction(transaction_id, amount)

        if success:
            return jsonify(success=True, message=message), 200
        else:
            return jsonify(success=False, message=message), 400

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500


