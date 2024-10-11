from ..models.consumerWeb import consumerWeb
from ..models.merchant import Merchant

class ConsumerWebController:
    def register_consumer(self, customer):
        return consumerWeb().createConsumer(customer)

    def send_transaction(self, cust_email, merch_email, amount):
        # Fetch consumer and merchant by their emails
        consumer, consumer_message = consumerWeb().getConsumerByEmail(cust_email)
        if not consumer:
            return False, consumer_message

        merchant, merchant_message = Merchant().getMerchantByEmail(merch_email)
        if not merchant:
            return False, merchant_message

        # Send transaction if both exist
        return consumerWeb().sendTransaction(consumer['cust_id'], merchant['merch_id'], amount)

    def getConsumerByEmail(self, cust_email):
        return consumerWeb().getConsumerByEmail(cust_email)