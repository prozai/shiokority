import pymysql
from flask import current_app, g
from ..auth.databaseConnection import getDBConnection

class Transaction():
    
    def viewPaymentRecordByMerchId(self, merch_id):
        # Fetch the transaction history for the merchant
        
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Payment_Record WHERE merch_id=%s"
                cursor.execute(sql, (merch_id))
                result = cursor.fetchall()

                return result
            
        except pymysql.MySQLError as e:
            print(f'Error Occur: {e}')
            return False
        
        finally:
            connection.close()