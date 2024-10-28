from ..models.bank import Bank

class BankController():

    def viewAllTransaction(self):
        return Bank().viewAllTransaction()
    
    def viewAllTransactionHistory(self):
        return Bank().viewAllTransactionHistory()

    def viewAllTransactionRecord(self):
        return Bank().viewAllTransactionRecord()