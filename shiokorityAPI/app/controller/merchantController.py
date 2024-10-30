from ..models.merchant import Merchant
from ..models.apiProcess import ApiProcess
from ..models.transaction import Transaction

class MerchantController:
    
    def registerMerchant(self, merchant):
        return Merchant().registerMerchant(merchant)

    def getMerchantByEmail(self, email):
        return Merchant().getMerchantByEmail(email)
    
    def getMerchantByID(self, merch_id):
        return Merchant().getMerchantByID(merch_id)
    
    def validateUEN(self, uen):
        return ApiProcess().validateUEN(uen)
    
    def viewPaymentRecordByMerchId(self, merch_id):
        return Transaction().viewPaymentRecordByMerchId(merch_id)
