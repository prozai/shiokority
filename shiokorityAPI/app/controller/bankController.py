from ..models.bank import Bank
from ..models.consumer import Consumer
from ..models.merchant import Merchant

class BankController:

    # def process_transaction(self, consumer_email, merch_email, amount):
    #     # Fetch consumer and merchant by email
    #     consumer = Consumer().getConsumerByEmail(consumer_email)
    #     if not consumer:
    #         return False, "Consumer not found"

    #     merchant = Merchant().getMerchantByEmail(merch_email)
    #     if not merchant:
    #         return False, "Merchant not found"

    #     # Process the transaction using the Bank model
    #     success, message = self.bank_model.processTransaction(consumer['consumer_id'], merchant['merch_id'], amount)
    #     return success, message
    pass