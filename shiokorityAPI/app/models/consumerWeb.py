import pymysql
from flask import current_app, g
import bcrypt

class consumerWeb:

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

    def registerConsumer(self, email, password, name, phone, address):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        connection = self.getDBConnection()

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Customer (cust_email, cust_pass, cust_name, cust_phone, cust_address, date_created, date_updated_on, status)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), 1)
                """
                cursor.execute(query, (email, hashed_password, name, phone, address))
                connection.commit()
                return True, "Consumer created successfully"
        except pymysql.MySQLError as e:
            return False, f"Error creating consumer: {e}"

    def login(self, email, password):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM Customer WHERE cust_email = %s"
                cursor.execute(query, (email,))
                consumer = cursor.fetchone()
                if consumer and bcrypt.checkpw(password.encode('utf-8'), consumer['cust_pass'].encode('utf-8')):
                    return True, consumer
                else:
                    return False, "Invalid email or password"
        except pymysql.MySQLError as e:
            return False, "Error logging in"

    def processPayment(self, consumer_email, merchant_id, amount):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Payment (consumer_email, merch_id, amount, payment_date, payment_status, date_created, date_updated_on)
                    VALUES (%s, %s, %s, NOW(), 'pending', NOW(), NOW())
                """
                cursor.execute(query, (consumer_email, merchant_id, amount))
                connection.commit()
                return True, "Payment processed"
        except pymysql.MySQLError as e:
            return False, f"Error processing payment: {e}"