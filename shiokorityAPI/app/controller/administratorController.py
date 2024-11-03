from ..models.administrator import Administrator
from ..models.merchant import Merchant
from ..models.consumer import Consumer
from ..models.auditTrail import AuditTrail

class AdminController:
    def validate_admin_login(self, email, password):
        return Administrator.validateLogin(email, password)

    def create_merchant(self, merchant):
        return Merchant().createMerchant(merchant)

    def get_merchant_data(self):
        return Merchant().getMerchantData()

    def get_one_merchant(self, merch_id):
        return Merchant().getOneMerchant(merch_id)

    def update_merchant_details(self, merch_id, data):
        return Merchant().updateMerchantDetails(merch_id, data)

    def update_merchant_status(self, merch_id, status):
        return Merchant().updateMerchantStatus(merch_id, status)
    
    def getAdminTokenByEmail(self, email):
        return Administrator().getAdminTokenByEmail(email)

    def update2FAbyEmail(self, email):
        return Administrator().update2FAbyEmail(email)

    def addUser(self, user):
        return Consumer().addUser(user)

    def get_all_users(self):
        return Consumer().get_all_users()

    def get_user_by_id(self, cust_id):
        return Consumer().getUserById(cust_id)

    def submit_user_update(self, user_id, email=None, first_name=None, last_name=None, address=None, phone=None, status=None):
        return Consumer().update_user(user_id, email, first_name, last_name, address, phone, status)

    def get_all_audit_trail_logs(self):
        return AuditTrail().get_all_logs()

    def get_log_by_id(self, audit_id):
        return AuditTrail().get_log_by_id(audit_id)
