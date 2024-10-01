from ..models.consumer import Consumer
from ..models.merchant import Merchant

class ConsumerController():

    def validateMerchant(self, merchant_id):
        return Merchant().validateMerchantIsValid(merchant_id)
    
    def process_payment(self, merchant_id, amount):
        return Consumer().process_payment(merchant_id, amount)