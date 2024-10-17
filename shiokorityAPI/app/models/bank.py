import pymysql
from flask import current_app
from ..auth.databaseConnection import getDBConnection

class Bank():

    def bankProcessPayment(self, cardNumber, amount):

        # Check if the customer exists
        isCustomerExists, customer = self.getCustomerIDByCardNumber(cardNumber)

        # If the customer does not exist, return an error message
        if not isCustomerExists:

            # If false, customer will be the error message
            return False, customer
        
        # If the customer exists, deduct the amount from the customer's account balance
        isDeducted, message = self.deductAmountFromCustomerAccount(customer['customer_id'], amount)

        if not isDeducted:
            return False, message

        # after deduct the amount from the customer's account balance, need to insert the transaction record into the bank.
        isInserted, transactionId = self.insertTransactionRecords(amount, customer['customer_id'])

        if not isInserted:
            # If false, transactionId will be the error message
            return False, message
        
        #after insert the transaction record, need to insert to transaction in shiokority_bank
        isInserted, message = self.insertTransaction(amount, customer['customer_id'], transactionId)

        if not isInserted:
            return False, message
        
        #after insert the transaction , need to insert to transaction_history in shiokority_bank

        isInserted, message = self.insertTransactionHistory(amount, customer['customer_id'], transactionId)

        if not isInserted:
            return False, message
        
        return True, "Payment processed successfully"



    def insertTransactionHistory(self, amount, customer_id, transaction_record_id):
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Transaction_history (transaction_history_amount, transaction_history_date, transaction_history_status,
                    customer_id, transaction_record_id)
                    VALUES (%s, NOW(), 'completed', %s, %s)
                '''
                result = cursor.execute(sql_query, (amount, customer_id, transaction_record_id))
                connection.commit()

                if result == 0:
                    return False, "Error inserting transaction record"
                
                return True, "Transaction inserted successfully"
            
        except Exception as e:
            print(f"Error inserting transaction history record function: {str(e)}")
            return False, "Error inserting transaction history record"
        
        finally:
            connection.close()

    def insertTransaction(self, amount, customer_id, transaction_record_id):
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Transaction (transaction_amount, transaction_date, transaction_status, 
                    customer_id, transaction_record_id)
                    VALUES (%s, NOW(), 'completed', %s, %s)
                '''
                result = cursor.execute(sql_query, (amount, customer_id, transaction_record_id))
                connection.commit()

                if result == 0:
                    return False, "Error inserting transaction record"
                
                return True, "Transaction inserted successfully"
            
        except Exception as e:
            print(f"Error inserting transaction function : {str(e)}")
            return False, "Error inserting transaction"
        
        finally:
            connection.close()



    def insertTransactionRecords(self, amount, customer_id):
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    INSERT INTO Transaction_record (transaction_record_amount, transaction_record_date,
                    transaction_record_status, customer_id)
                    VALUES (%s, NOW(), 'completed', %s)
                '''
                result = cursor.execute(sql_query, (amount, customer_id))
                transaction_record_pk = cursor.lastrowid
                connection.commit()

                if result == 0:
                    return False, "Error inserting transaction record"
                
                return True, transaction_record_pk
            
        except Exception as e:
            print(f"Error inserting transaction record function: {str(e)}")
            return False, "Error inserting transaction record"
        
        finally:
            connection.close()
        

    def deductAmountFromCustomerAccount(self, customer_id, amount):
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    UPDATE Customer
                    SET customer_bank_balance = customer_bank_balance - %s
                    WHERE customer_id = %s
                '''
                result = cursor.execute(sql_query, (amount, customer_id))
                connection.commit()

                if result == 0:
                    return False, "Error deducting amount from customer account"
                
                return True, "Amount deducted from customer account successfully"
            
        except Exception as e:
            print(f"Error deducting amount from customer account: {str(e)}")
            return False, "Error deducting amount from customer account"
        
        finally:
            connection.close()

        
    def getCustomerIDByCardNumber(self, cardNumber):
        connection = getDBConnection(current_app.config['BANK_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    SELECT customer_id FROM Card
                    WHERE pan = %s
                '''
                cursor.execute(sql_query, (cardNumber))
                customer = cursor.fetchone()

                if not customer:
                    return False, "Customer not found"
                

                return True, customer
        except Exception as e:
            print(f"Error fetching customer by card number: {str(e)}")
            return False, "Error fetching customer by card number"
        
        finally:
            connection.close()