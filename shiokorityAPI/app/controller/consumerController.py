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
    
    def processPayment(self, data):
        return Consumer().processPayment(data) 

    def getConsumerByEmail(self, cust_email):
        return Consumer().getConsumerByEmail(cust_email)
    
    def getConsumerByID(self, cust_id):
        return Consumer().getConsumerByID(cust_id)
    
    def customerValidateCardProcedure(self, card_number, cvv, expiry_date):
        return Consumer().customerValidateCardProcedure(card_number, cvv, expiry_date)    