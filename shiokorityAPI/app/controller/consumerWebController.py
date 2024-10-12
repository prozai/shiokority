<<<<<<< HEAD
from ..models.consumerWeb import Consumer
from ..models.merchant import Merchant

class ConsumerWebController:
    def register_consumer(self, consumer):
        return Consumer().createConsumer(consumer)

    def send_transaction(self, consumer_email, merch_email, amount):
        # Fetch consumer and merchant by their emails
        consumer, consumer_message = Consumer().getConsumerByEmail(consumer_email)
=======
from ..models.consumerWeb import consumerWeb
from ..models.merchant import Merchant

class ConsumerWebController:
    def register_consumer(self, customer):
        return consumerWeb().createConsumer(customer)

    def send_transaction(self, cust_email, merch_email, amount):
        # Fetch consumer and merchant by their emails
        consumer, consumer_message = consumerWeb().getConsumerByEmail(cust_email)
>>>>>>> c1bf434226944f602256a0d7343f0a468bf8b8a3
        if not consumer:
            return False, consumer_message

        merchant, merchant_message = Merchant().getMerchantByEmail(merch_email)
        if not merchant:
            return False, merchant_message

        # Send transaction if both exist
<<<<<<< HEAD
        return Consumer().sendTransaction(consumer['consumer_id'], merchant['merch_id'], amount)

    def get_consumer_by_email(self, consumer_email):
        return Consumer().getConsumerByEmail(consumer_email)
=======
        return consumerWeb().sendTransaction(consumer['cust_id'], merchant['merch_id'], amount)

    def getConsumerByEmail(self, cust_email):
        return consumerWeb().getConsumerByEmail(cust_email)
>>>>>>> c1bf434226944f602256a0d7343f0a468bf8b8a3
