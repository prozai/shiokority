from ..models.consumer import Consumer
from ..models.merchant import Merchant

class ConsumerController():

    def validateMerchant(self, merchant_id):
        return Merchant().validateMerchantIsValid(merchant_id)
    
    def process_payment(self, merchant_id, amount):
        return Consumer().process_payment(merchant_id, amount)

    def register_consumer(self, customer):
        return Consumer().createConsumer(customer)
    
    def login(self, cust_email, password):
        return Consumer().login(cust_email, password)
    
    def send_transaction(self, cust_email, merch_email, amount):
        # Fetch consumer and merchant by their emails
        consumer, consumer_message = Consumer().getConsumerByEmail(cust_email)
        if not consumer:
            return False, consumer_message

        merchant, merchant_message = Merchant().getMerchantByEmail(merch_email)
        if not merchant:
            return False, merchant_message

        # Send transaction if both exist
        return Consumer().sendTransaction(consumer['cust_id'], merchant['merch_id'], amount)

    def getConsumerByEmail(self, cust_email):
        return Consumer().getConsumerByEmail(cust_email)