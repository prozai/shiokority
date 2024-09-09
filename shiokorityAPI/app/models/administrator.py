import pymysql
from flask import current_app, jsonify
import bcrypt
from pymysql.err import MySQLError

class Administrator():
    
    # 227
    def validateLogin(email, password):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database='usermanagement',
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve the hashed password and status
                    sql_query = '''
                        SELECT admin_id, admin_username, pass_hash, status 
                        FROM admin 
                        WHERE admin_username = %s
                    '''
                    cursor.execute(sql_query, (email,))
                    user = cursor.fetchone()
                    
                    
                    if not user:
                        print(f"Login attempt failed: User not found for email {email}")
                        return False
                    
                    if user['status'] != 'active':
                        print(f"Login attempt failed: Inactive account for email {email}")
                        return False
                    
                    # Retrieve the hashed password from the database
                    hashed_password = user['pass_hash'].encode('utf-8')
                    
                    # Check if the provided password matches the hashed password
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                        print(f"Login successful for user {email}")
                        return True
                    
                    else:
                        print(f"Login attempt failed: Incorrect password for email {email}")
                        return False
                        

        except MySQLError as e:
            print(f"Database error during login validation: {str(e)}")
            raise

        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            raise
                
    # 143
    def createMerchant(merch_name,  merch_email, merch_phone):
        
        values = (merch_name,  merch_email, merch_phone)
        
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connect.cursor() as cursor:
                
                # Insert the new merchant
                sqlQuery = """
                    INSERT INTO merchant (merch_name,  merch_username, merch_phone, pass_hash, date_created, date_updated_on)
                    VALUES (%s, %s, %s, 1, NOW(), NOW())
                    """ 
                cursor.execute(sqlQuery, values)
                connect.commit()  
                return True  # Merchant created successfully
                
        except pymysql.MySQLError as e:
            print(f"Error creating merchant: {e}")
            return False  # Return False in case of an error
            
        finally:
            connect.close()  # Ensure the connection is closed
    
    def getMerchantData(self):
        
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connect.cursor() as cursor:
        
                sqlQuery = "SELECT * FROM merchantmanagement.merchant"
                cursor.execute(sqlQuery)
                
                merchant = cursor.fetchall()
                
                cursor.close()
                
                return merchant  # Merchant created successfully
                
        except pymysql.MySQLError as e:
            print(f"Error Fetching merchant: {e}")
            return False  # Return False in case of an error
            
        finally:
            connect.close()  # Ensure the connection is closed
            
    def getOneMerchant(self, id):
        
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connect.cursor() as cursor:
        
                sqlQuery = """SELECT * FROM merchantmanagement.merchant WHERE merch_id = %s"""
                cursor.execute(sqlQuery, id)
                
                merchant = cursor.fetchone()
                
                cursor.close()
                
                if merchant is None:
                    return False
                
                return merchant  # Merchant created successfully
                
        except pymysql.MySQLError as e:
            print(f"Error Fetching merchant: {e}")
            return False  # Return False in case of an error
            
        finally:
            connect.close()  # Ensure the connection is closed
        
    
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
    
    
    def updateMerchantStatus(self, merch_id):
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='merchantmanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connect.cursor() as cursor:
                # SQL query to delete the merchant by ID
                sql = "UPDATE merchant SET merch_status = false, date_updated_on = NOW() WHERE merch_id = %s"
                validate = cursor.execute(sql, (merch_id,))
                
                if validate == 0:
                    return False
            
            connect.commit()

            return True
        
        except Exception as e:
            connect.rollback()
            return False