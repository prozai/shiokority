from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from ..controller.consumerController import ConsumerController

consumerBlueprint = Blueprint('consumerBlueprint', __name__)

@consumerBlueprint.route('/consumer/process-payment', methods=['POST'])
def processPayment():
    try:
        data = request.get_json()

        merchant_id = data.get('merch_id')
        amount = data.get('amount')
        
        if merchant_id is None or amount is None:
            raise BadRequest("Merchant ID and amount are required")
        
        checkMerchant = ConsumerController().validateMerchant(merchant_id)

        if not checkMerchant:
            return jsonify(success=False, message="Merchant not found or not valid")
    
        paymentStatus = ConsumerController().process_payment(merchant_id, amount)

        return jsonify(paymentStatus)

    except BadRequest as e:
        return jsonify(success=False, message=str(e)), 400
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False, message="An unexpected error occurred"), 500