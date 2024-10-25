from ..models.merchant import Merchant
from ..models.apiProcess import ApiProcess

class MerchantController:
    
    def registerMerchant(self, merchant):
        return Merchant().registerMerchant(merchant)

    def getMerchantByEmail(self, email):
        return Merchant().getMerchantByEmail(email)
    
    def getMerchantByID(self, merch_id):
        return Merchant().getMerchantByID(merch_id)
    
    def updateMerchant(self, merch_id, merchant):
        return Merchant().updateMerchant(merch_id, merchant)
    
    def validateUEN(self, uen):
        return ApiProcess().validateUEN(uen)