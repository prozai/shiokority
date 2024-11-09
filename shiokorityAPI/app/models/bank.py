import pymysql
from flask import current_app
from ..auth.databaseConnection import getDBConnection

class Bank():

    def viewAllTransactionRecord(self):

        connection = getDBConnection(current_app.config['BANK_SCHEMA'])

        try:
            with connection.cursor() as cursor:

                sql = """SELECT * FROM Transaction_Record;"""
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error viewAllTransactionRecord: {e}")
            return "An error occurred"
    
    def viewAllTransactionHistory(self):

        connection = getDBConnection(current_app.config['BANK_SCHEMA'])

        try:
            with connection.cursor() as cursor:

                sql = """SELECT * FROM Transaction_History;"""
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error viewAllTransactionHistory: {e}")
            return "An error occurred"

    def viewAllTransaction(self):

        connection = getDBConnection(current_app.config['BANK_SCHEMA'])

        try:
            with connection.cursor() as cursor:

                sql = """SELECT * FROM Transaction;"""
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error viewAllTransaction: {e}")
            return "An error occurred"


    def bankProcessPayment(self, cardNumber, amount, uen):
        
        # This function will be called by the API to process the payment
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])

        try:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:

                # Prepare the output parameters as queryable variables
                cursor.callproc('ProcessPayment', [cardNumber, amount, uen, '','',''])

                # Retrieve output parameters (status_code and status_message and transaction_record_id)
                cursor.execute("SELECT @_ProcessPayment_3, @_ProcessPayment_4, @_ProcessPayment_5")
                result = cursor.fetchone()

                connection.commit()

                response = {
                    'statusCode': result['@_ProcessPayment_3'],
                    'statusMessage': result['@_ProcessPayment_4'],
                    'transactionRecordId': result['@_ProcessPayment_5']
                }

                if response['statusCode'] == 403 or response['statusCode'] == 404:
                    return False, response
                
                return True, response

        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error: {e}")
            return False, "An error occurred"

        finally:
            # Close the database connection
            connection.close()