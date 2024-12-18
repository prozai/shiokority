from ..auth.databaseConnection import getDBConnection
from flask import current_app
from .bank import Bank
import pymysql
from .fraudDetection import FraudDetection
from datetime import datetime, timedelta
from ..models.consumer import Consumer
from ..auth.CardTokenizer import CardTokenizer

class ApiProcess(): 

    def __init__(self):
        self.tokenizer = CardTokenizer()

    def validateCardProcedure(self, card_number, cvv, expiry_date):
        # Tokenize card here
        token = self.tokenizer.tokenize(card_number, cvv, expiry_date)

        if not token:
            return False, "Invalid card details"

        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:
                
                # Detokenize the card details include card number, cvv, and expiry date
                card = self.tokenizer.bank_detokenize(token)

                # Call the stored procedure with OUT parameters as placeholders
                cursor.callproc('CheckCardInBank', (card['card_number'], card['cvv'], card['expiry_date'], 0, ''))

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
        #data include cust_email, amount, cardNumber, expiryDate, cvv

        token = self.tokenizer.tokenize(data['cardNumber'], data['cvv'], data['expiryDate'])

        # fraud detection check
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        custId = Consumer().getConsumerByEmail(data['cust_email'])['cust_id']
        isFraud, message = FraudDetection().detect_transaction_fraud(custId, data['amount'], timestamp)

        if not isFraud:
            return isFraud, message

        
        # before process to bank, need to insert the payment record
        isInserted, response = self.beforeProcessToBank(data['uen'], data['cust_email'], token, data['cvv'], data['expiryDate'], data['amount'])

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

            return False, message
        

        # if the bank process payment is successful, insert the payment history and update the payment status
        isUpdated, message = self.afterProcessToBank(paymentRecordId, 'completed', token, merchId, bank_transactionRecordId, transactionId, paymentId)

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

        
    def beforeProcessToBank(self, uen, custEmail, cardNumber, cvv, expiryDate, amount):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])


        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Call the stored procedure with placeholder parameters
                cursor.callproc('BeforeProceedToBank', [
                    uen, custEmail, cardNumber, cvv, expiryDate, amount,
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
                    'merchId': result['merchId'],
                }

                return True, response

        except pymysql.MySQLError as e:
            # Handle any MySQL-related errors
            print(f"Error before process to bank function: {str(e)}")
            return False, "An error occurred during the bank processing"

        finally:
            # Ensure the connection is closed properly
            connection.close()

    def validateUEN(self, uen):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['GOVERNMENT_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with placeholder parameters
                cursor.callproc('validateUEN', [uen, ''])

                # Query to retrieve the OUT parameter values
                sql_query = '''
                    SELECT @_validateUEN_1 AS statusCode;
                '''
                cursor.execute(sql_query)
                result = cursor.fetchone()
                connection.commit()

                # Check the status code for error conditions
                statusCode = result['statusCode']
                if statusCode == 404:
                    # if the UEN is not valid, insert the payment authorise record
                    self.insertPaymentAuthorise(uen, 0)
                    return False

                # if the UEN is valid, insert the payment authorise record
                self.insertPaymentAuthorise(uen, 1)
                return True

        except pymysql.MySQLError as e:
            # Handle any MySQL-related errors
            print(f"Error in validate UEN function: {str(e)}")
            return False, "An error occurred during UEN validation"

        finally:
            # Ensure the connection is closed properly
            connection.close()
    
    def insertPaymentAuthorise(self, uen, status):
        # Establish a connection to the database
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with placeholder parameters
                cursor.callproc('InsertPaymentAuthorisation', [uen, status, ''])
                connection.commit()

        except pymysql.MySQLError as e:
            # Handle any MySQL-related errors
            print(f"Error in insert payment authorise function: {str(e)}")
            connection.rollback()

        finally:
            # Ensure the connection is closed properly
            connection.close()
