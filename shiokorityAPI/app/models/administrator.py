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