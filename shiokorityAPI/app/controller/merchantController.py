from ..models.merchant import Merchant

class MerchantController:
    
    def register_merchant(self, merchant):
        return Merchant().createMerchant(merchant)

    def login(self, merch_email, password):
        return Merchant().login(merch_email, password)

    def get_profile(self, merch_id):
        return Merchant().getMerchantByID(merch_id)

    def update_merchant_details(self, merch_id, data):
        return Merchant().updateMerchantDetails(merch_id, data)

    def process_payment(self, merch_email, amount):
        return Merchant().addPayment(merch_email, amount)

    def get_transaction_history(self, merch_id):
        return Merchant().getTransactionHistory(merch_id)

    def validate_merchant_status(self, merch_id):
        return Merchant().validateMerchantIsValid(merch_id)

    def logout_merchant(self, session):
        if 'merch_id' in session:
            session.pop('merch_id')
            return True, "Merchant logged out successfully"
        return False, "No merchant session found"

    def fetch_all_merchants(self):
        return Merchant().getMerchantData()

    def get_one_merchant(self, merch_id):
        return Merchant().getOneMerchant(merch_id)

    def update_merchant_status(self, merch_id, status):
        return Merchant().updateMerchantStatus(merch_id, status)