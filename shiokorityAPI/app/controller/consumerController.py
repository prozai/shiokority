from ..models.consumer import Consumer
from ..models.merchant import Merchant

class ConsumerController():

    # def validateMerchant(self, merchant_id):
    #     return Merchant().validateMerchantIsValid(merchant_id)
    
    # def process_payment(self, merchant_id, amount):
    #     return Consumer().process_payment(merchant_id, amount)

    def registerConsumer(self, customer):
        return Consumer().registerConsumer(customer)
    
    def login(self, cust_email, password):
        return Consumer().login(cust_email, password)
    
    def processPayment(self, cust_email, merch_email, amount):
        return Consumer().processPayment(cust_email, merch_email, amount) 

    def getConsumerByEmail(self, cust_email):
        return Consumer().getConsumerByEmail(cust_email)
    