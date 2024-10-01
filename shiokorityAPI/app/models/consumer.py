import pymysql
from flask import current_app
from pymysql.err import MySQLError

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
        