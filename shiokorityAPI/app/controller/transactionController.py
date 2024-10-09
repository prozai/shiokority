from ..models.transaction import Transaction

class TransactionController:

    def add_transaction(self, transaction_data):
        return Transaction().addTransaction(transaction_data)

    def get_transaction_history(self, customer_id):
        return Transaction().getTransactionHistory(customer_id)

    def update_transaction_status(self, transaction_id, status):
        return Transaction().updateTransactionStatus(transaction_id, status)