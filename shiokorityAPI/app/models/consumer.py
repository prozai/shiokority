import pymysql
from flask import current_app, g
from pymysql.err import MySQLError
import bcrypt
from .merchant import Merchant
from .transaction import Transaction
from ..auth.databaseConnection import getDBConnection

class Consumer():


    # def process_payment(self, merchant_id, amount):
    #     try:
    #         with pymysql.connect(
    #             host=current_app.config['MYSQL_HOST'],
    #             user=current_app.config['MYSQL_USER'],
    #             password=current_app.config['MYSQL_PASSWORD'],
    #             database=current_app.config['MERCHANT_SCHEMA'],
    #             cursorclass=pymysql.cursors.DictCursor
    #         ) as connection:
    #             with connection.cursor() as cursor:
    #                 # Process the payment
    #                 sql_query = """
    #                 UPDATE Merchant
    #                 SET merch_amount = merch_amount + %s 
    #                 WHERE merch_id = %s
    #                 """
    #                 cursor.execute(sql_query, (amount, merchant_id))
    #                 connection.commit()
    #                 return True

    #     except MySQLError as e:
    #         print(f"Database error during payment processing: {str(e)}")
    #         return False, "Database error occurred"

    #     except Exception as e:
    #         print(f"Unexpected error during payment processing: {str(e)}")
    #         return False, "An unexpected error occurred"

    def registerConsumer(self, customer):

        hash_pass = bcrypt.hashpw(customer['cust_pass'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        existing_consumer = self.getConsumerByEmail(customer['cust_email'])

        if existing_consumer:
            return False, "Email already in use"

        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    INSERT INTO Customer (cust_fname, cust_lname, cust_email, cust_pass, cust_address, cust_phone, date_created, date_updated_on, cust_status)
                    VALUES (%s, %s, %s, %s, %s, %s NOW(), NOW(), 1)
                """
                cursor.execute(sql_query, (customer['cust_fname'], customer['cust_lname'], customer['cust_email'], hash_pass, customer['cust_address'], customer['cust_phone']))
                connection.commit()
                return True, "Consumer created successfully"
            
        except pymysql.MySQLError as e:
            print(f"Error creating consumer: {e}")
            return False, f"Error creating consumer: {e}"

    def login(self, cust_email, cust_pass):
        connection = getDBConnection(current_app.config['PAY_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Customer WHERE cust_email = %s"
                cursor.execute(sql_query, (cust_email, cust_pass))
                consumer = cursor.fetchone()
                if consumer and bcrypt.checkpw(cust_pass.encode('utf-8'), consumer['cust_pass'].encode('utf-8')):
                    return True, consumer
                else:
                    return False, "Invalid email or password"
        except pymysql.MySQLError as e:
            return False, "Error logging in"

    def processPayment(self, cust_email, merch_email, merch_amount):
        
        #1. need to check if the shiokority_pay.Consumer has enough money
        #2. need to check if the shiokority_pay.Merchant exists
        #3. need to check if the shiokority_pay.Merchant is active
        #4. need to deduct the amount from the shiokority_pay.Consumer
        #5. need to update the amount to the shiokority_pay.Merchant
        #6. need to insert the transaction into the shiokority._api.Payment table
       
        # Check if the consumer has enough money
        consumer = self.getConsumerByEmail(cust_email)

        if not consumer:
            return False, "Consumer not found"
        
        if consumer['cust_amount'] < merch_amount:
            return False, "Insufficient funds"
        
        # Check if the merchant exists
        merchant = self.getMerchantByEmail(merch_email)

        if not merchant:
            return False, "Merchant not found"
        
        if merchant['merch_status'] != 1:
            return False, "Merchant is inactive"
        
        # Deduct the amount from the consumer
        success, message = self.customerDeductAmount(cust_email, merch_amount)

        if not success:
            return False, message
        
        # Update the amount to the merchant
        success, message = Merchant().updateMerchantBalance(merch_email, merch_amount)
        
        if not success:
            return False, message

        # Insert the transaction into the Payment table
        success, message = Transaction.insertPaymentTransaction(cust_email, merch_email, merch_amount)

        if not success:
            return False, message
        
        # connection = getDBConnection(current_app.config['PAY_SCHEMA'])
        # try:
        #     with connection.cursor() as cursor:
        #         sql_query = """
        #             UPDATE Merchant
        #             SET merch_amount = merch_amount + %s,
        #             date_updated_on = NOW(),
        #             cust_email = %s,
        #             payment_date = NOW(),
        #             payment_status = 1
        #             WHERE merch_email = %s;
        #         """
        #         cursor.execute(sql_query, (merch_amount, cust_email, merch_email))
        #         connection.commit()
                
        #         return True, "Payment processed"
        # except pymysql.MySQLError as e:
        #     print(f"Error processing payment: {e}")
        #     return False, f"Error processing payment: {e}"

    def getConsumerByEmail(self, cust_email):
        # Fetch consumer by email - used in login and create
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Customer WHERE cust_email = %s"
                cursor.execute(sql_query, (cust_email,))
                consumer = cursor.fetchone()  
                return consumer  # Consumer data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching consumer by email: {e}")
            return None
        
    def getConsumerByID(self, cust_id):
        # Fetch consumer by ID from the database
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT cust_id, cust_fname, cust_lname, cust_email, cust_phone, cust_address, cust_phone
                    FROM Customer 
                    WHERE cust_id = %s
                """
                cursor.execute(sql_query, (cust_id,))
                consumer = cursor.fetchone()

                if not consumer:
                    return None

                return consumer

        except pymysql.MySQLError as e:
            print(f"Error fetching consumer: {e}")
            return None
        
    def customerDeductAmount(self, cust_email, amount):
        # Deduct the amount from the consumer
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    UPDATE Customer
                    SET cust_amount = cust_amount - %s
                    WHERE cust_email = %s
                """
                cursor.execute(sql_query, (amount, cust_email))
                connection.commit()
                return True, "Amount deducted successfully"
        except pymysql.MySQLError as e:
            print(f"Error deducting amount: {e}")
            return False, f"Error deducting amount: {e}"