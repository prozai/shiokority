from ..auth.databaseConnection import getDBConnection
from flask import current_app
from .bank import Bank
import pymysql

class ApiProcess(): 

    def validateCardProcedure(self, card_number, cvv, expiry_date):

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:

                # Prepare the output parameters as queryable variables
                cursor.callproc('CheckCardInBank', [card_number, cvv, expiry_date, 0, ''])

                # Retrieve output parameters (status_code and status_message)
                cursor.execute("SELECT @_CheckCardInBank_3, @_CheckCardInBank_4")
                result = cursor.fetchone()
                connection.commit()

                statusCode = result['@_CheckCardInBank_3']
                statusMessage = result['@_CheckCardInBank_4']


                if statusCode == 403 or statusCode == 404:
                    return False, statusMessage
                
                return True, statusMessage

        except pymysql.MySQLError as e:
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

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                cursor.callproc('AfterProceedToBank', [paymentRecordId, paymentStatus, cardNumber, merchId, transactionRecordId, transactionId, paymentId, '',''])
                
                sql_query = '''
                    SELECT @_AfterProceedToBank_7, @_AfterProceedToBank_8
                '''
                cursor.execute(sql_query)
                result = cursor.fetchone()
                connection.commit()
                
                response = {
                    'statusCode': result['@_AfterProceedToBank_7'],
                    'statusMessage': result['@_AfterProceedToBank_8']
                }

                
                return True, response['statusMessage']


        except Exception as e:
            print(f"Error after process to bank function: {str(e)}")
            return False, "Error after process to bank"
        
    def beforeProcessToBank(self, merchEmail, custEmail, cardNumber, cvv, expirtyDate, amount):

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                cursor.callproc('BeforeProceedToBank', [merchEmail, custEmail,cardNumber, cvv, expirtyDate, amount,
                                                        '', '', '', '', '', '', ''])
                
                sql_query = '''
                    SELECT @_BeforeProceedToBank_6, @_BeforeProceedToBank_7, @_BeforeProceedToBank_8, 
                    @_BeforeProceedToBank_9, @_BeforeProceedToBank_10,
                    @_BeforeProceedToBank_11, @_BeforeProceedToBank_12;
                '''
                cursor.execute(sql_query)
                result = cursor.fetchone()
                connection.commit()

                if result['@_BeforeProceedToBank_6'] == 403 or result['@_BeforeProceedToBank_6'] == 404: 
                    return False, result['@_BeforeProceedToBank_7']
                
                response = {
                    'paymentRecordId': result['@_BeforeProceedToBank_8'],
                    'transactionId': result['@_BeforeProceedToBank_9'],
                    'companyUEN': result['@_BeforeProceedToBank_10'],
                    'paymentId' : result['@_BeforeProceedToBank_11'],
                    'merchId' : result['@_BeforeProceedToBank_12']
                }
                
                return True, response

        except Exception as e:
            print(f"Error before process to bank function: {str(e)}")
            return False, "Error before process to bank"