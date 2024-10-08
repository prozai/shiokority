from ..models.consumer import Consumer
from ..models.merchant import Merchant

class ConsumerController:
    def register_consumer(self, consumer):
        return Consumer().createConsumer(consumer)

    def send_transaction(self, consumer_email, merch_email, amount):
        # Fetch consumer and merchant by their emails
        consumer, consumer_message = Consumer().getConsumerByEmail(consumer_email)
        if not consumer:
            return False, consumer_message

        merchant, merchant_message = Merchant().getMerchantByEmail(merch_email)
        if not merchant:
            return False, merchant_message

        # Send transaction if both exist
        return Consumer().sendTransaction(consumer['consumer_id'], merchant['merch_id'], amount)

    def get_consumer_by_email(self, consumer_email):
        return Consumer().getConsumerByEmail(consumer_email)