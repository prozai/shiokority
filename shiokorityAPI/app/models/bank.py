import pymysql
from flask import current_app

class Bank:

    def __init__(self):
        self.connection = None

    def getDBConnection(self):
        # Check if the database connection already exists
        if not self.connection:
            self.connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return self.connection

    def processTransaction(self, consumer_id, merch_id, amount):
        """Process a payment transaction between consumer and merchant."""
        try:
            connection = self.getDBConnection()

            with connection.cursor() as cursor:
                # Record the transaction in the transaction table
                sql_query = """
                    INSERT INTO transaction_management.Transaction (consumer_id, merch_id, amount, payment_date, status, date_created, date_updated_on)
                    VALUES (%s, %s, %s, NOW(), 'completed', NOW(), NOW())
                """
                cursor.execute(sql_query, (consumer_id, merch_id, amount))
                connection.commit()

            return True, "Transaction processed successfully"

        except pymysql.MySQLError as e:
            print(f"Error processing transaction: {e}")
            return False, f"Error processing transaction: {e}"

    def refundTransaction(self, payment_id, amount, merch_id):
        """Refund a specific transaction."""
        try:
            connection = self.getDBConnection()

            with connection.cursor() as cursor:
                # Update the transaction status to 'refunded' and deduct the amount from the merchant balance
                refund_query = """
                    UPDATE transaction_management.Transaction 
                    SET status = 'refunded' 
                    WHERE payment_id = %s
                """
                cursor.execute(refund_query, (payment_id,))
                
                # Update the merchant's balance
                update_balance_query = """
                    UPDATE merchant_management.Merchant 
                    SET merch_amount = merch_amount - %s 
                    WHERE merch_id = %s
                """
                cursor.execute(update_balance_query, (amount, merch_id))
                connection.commit()

            return True, "Transaction refunded successfully"

        except pymysql.MySQLError as e:
            print(f"Error processing refund: {e}")
            return False, f"Error processing refund: {e}"

    def getTransactionById(self, payment_id):
        """Fetch a transaction by its payment ID."""
        try:
            connection = self.getDBConnection()

            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM transaction_management.Transaction WHERE payment_id = %s"
                cursor.execute(sql_query, (payment_id,))
                transaction = cursor.fetchone()

                if not transaction:
                    return None

                return transaction

        except pymysql.MySQLError as e:
            print(f"Error fetching transaction: {e}")
            return None

    def getMerchantBalance(self, merch_id):
        """Fetch the balance of a specific merchant."""
        try:
            connection = self.getDBConnection()

            with connection.cursor() as cursor:
                sql_query = "SELECT merch_amount FROM merchant_management.Merchant WHERE merch_id = %s"
                cursor.execute(sql_query, (merch_id,))
                result = cursor.fetchone()

                if not result:
                    return None

                return result['merch_amount']

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant balance: {e}")
            return None