from ..models.consumer import Consumer
from ..models.merchant import Merchant

class ConsumerController():

    def validateMerchant(self, merchant_id):
        return Merchant().validateMerchantIsValid(merchant_id)
    
    def process_payment(self, merchant_id, amount):
        return Consumer().process_payment(merchant_id, amount)

    def registerConsumer(self, customer):
        return Consumer().registerConsumer(customer)
    
    def login(self, cust_email, password):
        return Consumer().login(cust_email, password)
    
    def sendPayment(self, cust_email, merch_email, merch_amount):
        # Fetch consumer and merchant by their emails
        consumer = Consumer().getConsumerByEmail(cust_email)
        if not consumer:
            return False, "Consumer not found"

        merchant = Merchant().getMerchantByEmail(merch_email)
        if not merchant:
            return False, "Merchant not found"

        # Send transaction if both exist
        return Consumer().sendPayment(consumer['cust_email'], merchant['merch_email'], merch_amount)

    def getConsumerByEmail(self, cust_email):
        return Consumer().getConsumerByEmail(cust_email)