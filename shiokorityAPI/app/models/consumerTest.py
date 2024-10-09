import pymysql
from flask import current_app

class Consumer:
    def createConsumer(self, consumer_name, consumer_email):
        try:
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                sql_query = """
                    INSERT INTO Consumer (consumer_name, consumer_email, date_created, date_updated_on)
                    VALUES (%s, %s, NOW(), NOW())
                """
                cursor.execute(sql_query, (consumer_name, consumer_email))
                connection.commit()
                return True, "Consumer created successfully"
        except pymysql.MySQLError as e:
            print(f"Error creating consumer: {e}")
            return False, f"Error: {e}"

    def getConsumerByEmail(self, consumer_email):
        try:
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Consumer WHERE consumer_email = %s"
                cursor.execute(sql_query, (consumer_email,))
                consumer = cursor.fetchone()

                if consumer is None:
                    return False, "Consumer not found"

                return consumer, "Consumer found"
        except pymysql.MySQLError as e:
            print(f"Error fetching consumer: {e}")
            return None, f"Error: {e}"

    def sendTransaction(self, consumer_id, merch_id, amount):
        try:
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                sql_query = """
                    INSERT INTO transaction_management.Transaction (consumer_id, merch_id, amount, payment_date, status, date_created, date_updated_on)
                    VALUES (%s, %s, %s, NOW(), 'completed', NOW(), NOW())
                """
                cursor.execute(sql_query, (consumer_id, merch_id, amount))
                connection.commit()

                return True, "Transaction completed successfully"
        except pymysql.MySQLError as e:
            print(f"Error sending transaction: {e}")
            return False, f"Error: {e}"