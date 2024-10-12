import pymysql
from flask import current_app, g
from pymysql.err import MySQLError
import bcrypt

class Consumer():


    def process_payment(self, merchant_id, amount):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MERCHANT_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Process the payment
                    sql_query = """
                    UPDATE Merchant
                    SET merch_amount = merch_amount + %s 
                    WHERE merch_id = %s
                    """
                    cursor.execute(sql_query, (amount, merchant_id))
                    connection.commit()
                    return True

        except MySQLError as e:
            print(f"Database error during payment processing: {str(e)}")
            return False, "Database error occurred"

        except Exception as e:
            print(f"Unexpected error during payment processing: {str(e)}")
            return False, "An unexpected error occurred"
        
    def getDBConnection(self):
        if 'db' not in g:
            g.db = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return g.db

    def registerConsumer(self, cust_email, cust_pass, cust_fname, cust_lname, cust_phone, cust_address):

        hash_pass = bcrypt.hashpw(cust_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        existing_consumer = self.getConsumerByEmail(cust_email)

        if existing_consumer:
            return False, "Email already in use"

        try:
            connection = self.getDBConnection()
            with connection.cursor() as cursor:
                sql_query = """
                    INSERT INTO Customer (cust_email, cust_pass, cust_fname, cust_lname, cust_phone, cust_address, date_created, date_updated_on, cust_status)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), 1)
                """
                cursor.execute(sql_query, (cust_email, hash_pass, cust_fname, cust_lname, cust_phone, cust_address))
                connection.commit()
                return True, "Consumer created successfully"
            
        except pymysql.MySQLError as e:
            print(f"Error creating consumer: {e}")
            return False, f"Error creating consumer: {e}"

    def login(self, cust_email, cust_pass):
        connection = self.getDBConnection()
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

    def sendPayment(self, cust_email, merch_email, merch_amount):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                sql_query = """
                    UPDATE Merchant
                    SET merch_amount =  merch_amount + %s ,
                    date_updated_on = NOW(),
                    cust_email = %s,
                    payment_date = NOW(),
                    payment_status = 'pending'
                    WHERE merch_email = %s
                """
                cursor.execute(sql_query, (cust_email, merch_email, merch_amount))
                connection.commit()
                return True, "Payment processed"
        except pymysql.MySQLError as e:
            return False, f"Error processing payment: {e}"

    def getConsumerByEmail(self, cust_email):
        # Fetch consumer by email - used in login and create
        try:
            connection = self.getDBConnection()
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
            connection = self.getDBConnection()
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