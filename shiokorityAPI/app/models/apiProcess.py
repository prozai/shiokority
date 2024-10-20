from ..auth.databaseConnection import getDBConnection
from flask import current_app
from .bank import Bank
import pymysql

class ApiProcess(): 

    def validateCardProcedure(self, card_number, cvv, expiry_date):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:
                # Call the stored procedure with OUT parameters as placeholders
                cursor.callproc('CheckCardInBank', (card_number, cvv, expiry_date, 0, ''))

                # Retrieve the OUT parameter values using the positional names
                cursor.execute("SELECT @_CheckCardInBank_3 AS statusCode, @_CheckCardInBank_4 AS statusMessage")
                result = cursor.fetchone()

                # Commit the transaction
                connection.commit()

                # Extract the output values
                statusCode = result['statusCode']
                statusMessage = result['statusMessage']

                # Determine the return based on the status code
                if statusCode in (403, 404):
                    return False, statusMessage

                return True, statusMessage

        except pymysql.MySQLError as e:
            # Rollback in case of error
            connection.rollback()
            print(f"Error: {e}")
            return False, "An error occurred"

        finally:
            # Close the database connection
            connection.close()

    
    def paymentProcessProcedure(self, data):

        #data include cust_email, merch_email, amount, cardNumber, expiryDate, cvv
        
        # before process to bank, need to insert the payment record
        isInserted, response = self.beforeProcessToBank(data['merch_email'], data['cust_email'], data['cardNumber'], data['cvv'], data['expiryDate'], data['amount'])

        if not isInserted:
            # if the payment record is not inserted, return the error message from response
            return False, response
        
        paymentRecordId = response['paymentRecordId']
        uen = response['companyUEN']
        transactionId = response['transactionId']
        paymentId = response['paymentId']
        merchId = response['merchId']


        # if all the above steps are successful, now we need to call the bank to process the payment
        bankProcessPayment, message = Bank().bankProcessPayment(data['cardNumber'], data['amount'], uen)

        # bank will also return the transaction record id failed or successful
        bank_transactionRecordId = message['transactionRecordId']

        if not bankProcessPayment:

            # if the bank process payment is not successful, insert the payment history and update the payment status
            isUpdated, message = self.afterProcessToBank(paymentRecordId, 'failed', data['cardNumber'], merchId, bank_transactionRecordId, transactionId, paymentId)

            return isUpdated, message
        

        # if the bank process payment is successful, insert the payment history and update the payment status
        isUpdated, message = self.afterProcessToBank(paymentRecordId, 'completed', data['cardNumber'], merchId, bank_transactionRecordId, transactionId, paymentId)

        return isUpdated, message

    def afterProcessToBank(self, paymentRecordId, paymentStatus, cardNumber, merchId, transactionRecordId, transactionId, paymentId):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with the provided parameters
                cursor.callproc('AfterProceedToBank', [
                    paymentRecordId, paymentStatus, cardNumber, merchId, 
                    transactionRecordId, transactionId, paymentId, '', ''
                ])

                # Query to retrieve the OUT parameter values
                sql_query = '''
                    SELECT @_AfterProceedToBank_7 AS statusCode, @_AfterProceedToBank_8 AS statusMessage;
                '''
                cursor.execute(sql_query)
                result = cursor.fetchone()

                # Commit the transaction
                connection.commit()

                # Prepare the response with the retrieved status code and message
                response = {
                    'statusCode': result['statusCode'],
                    'statusMessage': result['statusMessage']
                }

                # Return the status message along with a success indicator
                return True, response['statusMessage']

        except pymysql.MySQLError as e:
            # Handle any MySQL-related errors
            print(f"Error in after process to bank function: {str(e)}")
            return False, "An error occurred during post-bank processing"

        finally:
            # Ensure the connection is closed properly
            connection.close()

        
    def beforeProcessToBank(self, merchEmail, custEmail, cardNumber, cvv, expiryDate, amount):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Call the stored procedure with placeholder parameters
                cursor.callproc('BeforeProceedToBank', [
                    merchEmail, custEmail, cardNumber, cvv, expiryDate, amount,
                    '', '', '', '', '', '', ''
                ])

                # Query to retrieve the OUT parameter values
                sql_query = '''
                    SELECT @_BeforeProceedToBank_6 AS statusCode, @_BeforeProceedToBank_7 AS statusMessage, 
                        @_BeforeProceedToBank_8 AS paymentRecordId, @_BeforeProceedToBank_9 AS transactionId, 
                        @_BeforeProceedToBank_10 AS companyUEN, @_BeforeProceedToBank_11 AS paymentId, 
                        @_BeforeProceedToBank_12 AS merchId;
                '''
                cursor.execute(sql_query)
                result = cursor.fetchone()

                # Commit the transaction
                connection.commit()

                # Check the status code for error conditions
                statusCode = result['statusCode']
                statusMessage = result['statusMessage']
                if statusCode in (403, 404):
                    return False, statusMessage

                # Prepare the response with the retrieved values
                response = {
                    'paymentRecordId': result['paymentRecordId'],
                    'transactionId': result['transactionId'],
                    'companyUEN': result['companyUEN'],
                    'paymentId': result['paymentId'],
                    'merchId': result['merchId']
                }

                return True, response

        except pymysql.MySQLError as e:
            # Handle any MySQL-related errors
            print(f"Error before process to bank function: {str(e)}")
            return False, "An error occurred during the bank processing"

        finally:
            # Ensure the connection is closed properly
            connection.close()
