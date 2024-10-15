import pymysql
from flask import current_app, g
from ..auth.databaseConnection import getDBConnection

class Bank():

    def validateCard(self, card_number, cvv, expiry_date):
        try:
            connection = getDBConnection(current_app.config['BANK_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT card_id
                    FROM Card
                    WHERE card_number = %s
                """
                cursor.execute(sql_query, (card_number))
                card = cursor.fetchone()

                if not card:
                    print("Card not found")
                    return False, "Card not found"

                return True, "Card found"

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, "An unexpected error occurred"
    