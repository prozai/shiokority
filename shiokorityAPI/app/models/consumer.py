import pymysql
from flask import current_app
import bcrypt
from .merchant import Merchant
from .transaction import Transaction
from ..auth.databaseConnection import getDBConnection
from decimal import Decimal
from pymysql.err import MySQLError

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

    def processPayment(self, data):
        #0. need to check if the shiokority_pay.Consumer exists
        #1. need to check if the shiokority_pay.Consumer has enough money
        #2. need to check if the shiokority_pay.Merchant exists
        #3. need to check if the shiokority_pay.Merchant is active
        #4. need to deduct the amount from the shiokority_pay.Consumer
        #5. need to update the amount to the shiokority_pay.Merchant
        #6. need to insert the transaction into the shiokority._api.Payment table
       
        # Check if the consumer has enough money and Check if the consumer exists
        consumer = self.getConsumerByEmail(data['cust_email'])

        if not consumer:
            print("Consumer not found")
            return False, "Consumer not found"

        if consumer['cust_amount'] < Decimal(data['amount']):
            print("Insufficient funds")
            return False, "Insufficient funds"
        
        # Check if the merchant exists
        merchant = Merchant().getMerchantByEmail(data['merch_email'])

        if not merchant:
            print("Merchant not found")
            return False, "Merchant not found"
        
        if merchant['merch_status'] != 1:
            print("Merchant is inactive")
            return False, "Merchant is inactive"
        
        # Deduct the amount from the consumer
        success, message = self.customerDeductAmount(data['cust_email'], data['amount'])

        if not success:
            print("Error deducting amount")
            return False, message
        
        # Update the amount to the merchant
        success, message = Merchant().updateMerchantBalance(data['merch_email'], data['amount'])
        
        if not success:
            print("Error updating merchant balance")
            return False, message
        
        transactionData = {
            'amount': data['amount'],
            'cust_id': consumer['cust_id'],
            'merch_id': merchant['merch_id']
        }

        # Insert the transaction into the Payment table
        success, message = Transaction().insertPaymentTransaction(transactionData)

        if not success:
            return False, message
        
        return True, "Payment processed successfully"
    

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
                    SELECT 
                    *
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
        
    def customerValidateCardProcedure(self, card_number, cvv, expiry_date):

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            # Create a cursor to interact with the database
            with connection.cursor() as cursor:

                # Prepare the output parameters as queryable variables
                cursor.callproc('CheckCardInBothSchemas', [card_number, card_number, cvv, cvv, 0, ''])

                # Retrieve output parameters (status_code and status_message)
                cursor.execute("SELECT @_CheckCardInBothSchemas_4, @_CheckCardInBothSchemas_5")
                result = cursor.fetchone()

                statusCode = result['@_CheckCardInBothSchemas_4']
                statusMessage = result['@_CheckCardInBothSchemas_5']

                if statusCode == 403 or statusCode == 404:
                    return False, statusMessage
                
                return True, statusMessage

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return False, "An error occurred"

        finally:
            # Close the database connection
            connection.close()

    # My work of art
    #136
    def addUser(self, user):
        connection = None
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Hash the password before storing
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            with connection.cursor() as cursor:
                # Insert the new user into the Admin table
                sql_query = '''
                    INSERT INTO Customer (cust_email, cust_pass, cust_fname, cust_lname, cust_status, cust_address, cust_phone, date_created, date_updated_on)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(),NOW())
                '''
                cursor.execute(sql_query, (user['email'], hashed_password, user['first_name'], user['last_name'], user['status'], user['address'], user['phone']))
                connection.commit()
                return True

        except MySQLError as e:
            print(f"Database error during user creation: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during user creation: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()  # Ensure the connection is closed after the operation

    #137
    def get_all_users(self):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connect:
                with connect.cursor() as cursor:
                    sqlQuery = "SELECT * FROM Customer"
                    cursor.execute(sqlQuery)
                    users = cursor.fetchall()
                if not users:
                    return False
                return users
        except pymysql.MySQLError as e:
            print(f"Error fetching users: {e}")
            return False

    def getUserById(self, user_id):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve user details by user_id
                    sql_query = '''
                        SELECT cust_id, cust_email, cust_fname, cust_lname, cust_status, cust_address, cust_phone, date_created, date_updated_on
                        FROM Customer
                        WHERE cust_id = %s
                    '''
                    cursor.execute(sql_query, (user_id,))
                    user = cursor.fetchone()
                    
                    # Return the user data if found, otherwise None
                    if user:
                        return user
                    else:
                        return False
        except MySQLError as e:
            print(f"Database error during user retrieval: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error during user retrieval: {str(e)}")
            return False

    #141
    #138
    def update_user(self, cust_id, email=None, first_name=None, last_name=None, address=None, phone=None, status=None):
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Construct SQL query based on provided fields
            updates = []
            params = []

            if email:
                updates.append("cust_email = %s")
                params.append(email)

            if first_name:
                updates.append("cust_fname = %s")
                params.append(first_name)

            if last_name:
                updates.append("cust_lname = %s")
                params.append(last_name)

            if address:
                updates.append("cust_address = %s")
                params.append(address)

            if phone:
                updates.append("cust_phone = %s")
                params.append(phone)

            if status is not None:
                updates.append("cust_status = %s")
                params.append(status)

            # Ensure there are fields to update
            if not updates:
                return False

            # Add the `date_updated_on` field
            updates.append("date_updated_on = NOW()")

            params.append(cust_id)

            # Prepare the SQL query
            sql_query = f"UPDATE Customer SET {', '.join(updates)} WHERE cust_id = %s"

            with connection.cursor() as cursor:
                # Execute the query with the provided params
                cursor.execute(sql_query, params)
                connection.commit()
                return cursor.rowcount > 0  # Return True if any row was updated

        except MySQLError as e:
            print(f"Database error during user update: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during user update: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()