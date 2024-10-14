import pymysql
from flask import current_app, g
from ..auth.databaseConnection import getDBConnection

class Transaction():

    def insertPaymentTransaction(self, transaction_data):
        connection = getDBConnection(current_app.config['API_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                # Insert the transaction record
                query = """
                    INSERT INTO Transaction (transaction_amount, transaction_date, transaction_status, cust_id, merch_id)
                    VALUES (%s, NOW(), 'completed',%s, %s)
                """
                cursor.execute(query, (transaction_data['amount'], transaction_data['cust_id'], transaction_data['merch_id']))
                connection.commit()
                return True, "Transaction added successfully"
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error adding transaction: {e}")
            return False, f"Error adding transaction: {e}"
        finally:
            connection.close()

    def addTransaction(self, transaction_data):
        connection = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['BANK_SCHEMA'],  # Adjust schema name as per your structure
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # Insert the transaction record
                query = """
                    INSERT INTO Transaction_Record (transaction_record_id, transaction_record_amount, trasaction_record_date, transaction_record_status, customer_id)
                    VALUES (%s, %s, NOW(), %s, %s)
                """
                cursor.execute(query, (transaction_data['transaction_record_id'], transaction_data['amount'], 'completed', transaction_data['customer_id']))
                connection.commit()
                return True, "Transaction added successfully"
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error adding transaction: {e}")
            return False, f"Error adding transaction: {e}"
        finally:
            connection.close()

    def getTransactionHistory(self, customer_id):
        connection = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['BANK_SCHEMA'],  # Adjust schema name as per your structure
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT transaction_record_id, transaction_record_amount, trasaction_record_date, transaction_record_status
                    FROM Transaction_Record
                    WHERE customer_id = %s
                """
                cursor.execute(query, (customer_id,))
                transactions = cursor.fetchall()

                if not transactions:
                    return None, 0.0  # No transactions found

                # Optionally, you can calculate total balance here
                total_balance = sum([t['transaction_record_amount'] for t in transactions])
                return transactions, total_balance
        except pymysql.MySQLError as e:
            print(f"Error fetching transaction history: {e}")
            return None, 0.0
        finally:
            connection.close()

    def updateTransactionStatus(self, transaction_id, status):
        connection = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['BANK_SCHEMA'],
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                query = "UPDATE Transaction_Record SET transaction_record_status = %s WHERE transaction_record_id = %s"
                cursor.execute(query, (status, transaction_id))
                connection.commit()
                return True, "Transaction status updated successfully"
        except pymysql.MySQLError as e:
            print(f"Error updating transaction status: {e}")
            return False, f"Error updating transaction status: {e}"
        finally:
            connection.close()