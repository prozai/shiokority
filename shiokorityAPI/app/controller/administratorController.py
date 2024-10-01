from ..models.administrator import Administrator
from ..models.merchant import Merchant

class AdminController:
    def validate_admin_login(self, email, password):
        return Administrator.validateLogin(email, password)

    def create_merchant(self, name, email, phone, address):
        return Merchant().createMerchant(name, email, phone, address)

    def get_merchant_data(self):
        return Merchant().getMerchantData()

    def get_one_merchant(self, merch_id):
        return Merchant().getOneMerchant(merch_id)

    def update_merchant_details(self, merch_id, data):
        return Merchant().updateMerchantDetails(merch_id, data)

    def update_merchant_status(self, merch_id, status):
        return Merchant().updateMerchantStatus(merch_id, status)


    #My work
    def addUser(self,email, password, first_name, last_name, status):
        return Administrator().addUser(email, password, first_name, last_name, status)

    # New method to fetch all users
    def get_all_users(self):
        try:
            return Administrator.get_all_users(self)
        except Exception as e:
            print(f"Error fetching users in AdminController: {str(e)}")
            raise

    def submit_user_update(self, user_id, email=None, first_name=None, last_name=None, status=None):
        return Administrator().update_user(user_id, email, first_name, last_name, status)

    