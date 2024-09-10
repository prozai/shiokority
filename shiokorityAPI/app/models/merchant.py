import pymysql
from flask import current_app

class Merchant():

    # 143
    def createMerchant(merch_name, merch_email, merch_phone, merch_address):
        values = (merch_name, merch_email, merch_phone, merch_address)
        
        try:
            with pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor) as connect:
                # Insert the new merchant
                sqlQuery = """
                    INSERT INTO merchant (merch_name, merch_email, merch_phone, merch_address, pass_hash, date_created, date_updated_on)
                    VALUES (%s, %s, %s, %s, 1, NOW(), NOW())
                    """ 
                with connect.cursor() as cursor:
                    cursor.execute(sqlQuery, values)
                    connect.commit()  
                return True  # Merchant created successfully
                
        except pymysql.MySQLError as e:
            print(f"Error creating merchant: {e}")
            return False  # Return False in case of an error
            
    # 144
    def getMerchantData(self):
        try:
            with pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor) as connect:
                
                with connect.cursor() as cursor:
                    sqlQuery = "SELECT * FROM merchant"
                    cursor.execute(sqlQuery)
                    merchant = cursor.fetchall()
                
                if not merchant:
                    return False  # No merchant data found
                
                return merchant  # Merchant data fetched successfully
            
        except pymysql.MySQLError as e:
            print(f"Error fetching merchant data: {e}")
            return False  # Return False in case of an error

    def getOneMerchant(self, id):
        try:
            with pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor) as connect:
                with connect.cursor() as cursor:
                    sqlQuery = "SELECT * FROM merchant WHERE merch_id = %s"
                    cursor.execute(sqlQuery, id)
                    merchant = cursor.fetchone()
                
                if merchant is None:
                    return False
                
                return merchant  # Merchant fetched successfully
            
        except pymysql.MySQLError as e:
            print(f"Error fetching merchant: {e}")
            return False  # Return False in case of an error
        
    
    # 146
    def updateMerchantDetails(self, merchID,merchData):
        
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        try:
            
            query = """UPDATE merchantmanagement.merchant 
                    SET merch_name = %s, merch_username = %s, merch_phone = %s, date_updated_on = NOW()
                    WHERE merch_id = %s"""
            
            with connect.cursor() as cursor:
                affected_rows = cursor.execute(query, (merchData['merch_name'], merchData['merch_username'], merchData['merch_phone'], merchID))
                connect.commit()
            
            #not found
            if affected_rows == 0:
                return False
            
            return True
        
        except pymysql.MySQLError as e:
            connect.rollback()
            return False

        except Exception as e:
            return False