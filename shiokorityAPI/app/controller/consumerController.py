from ..models.consumer import Consumer
from ..models.merchant import Merchant
from ..models.apiProcess import ApiProcess

class ConsumerController():

    def registerConsumer(self, customer):
        return Consumer().registerConsumer(customer)
    
    def login(self, cust_email, password):
        return Consumer().login(cust_email, password)

    def getConsumerByEmail(self, cust_email):
        return Consumer().getConsumerByEmail(cust_email)
    
    def getConsumerByID(self, cust_id):
        return Consumer().getConsumerByID(cust_id)
    
    def customerValidateCardProcedure(self, card_number, cvv, expiry_date):
        return ApiProcess().validateCardProcedure(card_number, cvv, expiry_date) 
    
    def processPaymentProcedure(self, data):
        return ApiProcess().paymentProcessProcedure(data)
    
    def validateUEN(self, uen):
        return ApiProcess().validateUEN(uen)

    def get_merchant_data(self):
        return Merchant().getMerchantData()