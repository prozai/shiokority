import pymysql
from flask import current_app
import bcrypt
from pymysql.err import MySQLError
from ..auth.databaseConnection import getDBConnection
from ..models.fraudDetection import FraudDetection

class Administrator():
    # 227
    def validateLogin(email, password):
        
        connection = getDBConnection(current_app.config['ADMIN_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Query to retrieve the hashed password and status
                sql_query = '''
                    SELECT admin_id, admin_email, admin_pass, admin_account_status 
                    FROM Admin 
                    WHERE admin_email = %s
                '''
                cursor.execute(sql_query, (email,))
                user = cursor.fetchone()
                
                
                if not user:
                    print(f"Login attempt failed: User not found for email {email}")
                    return False, "User not found "
                
                if user['admin_account_status'] != 1:
                    print(f"Login attempt failed: Inactive account for email {email}")
                    return False, "Inactive account"
                
                # Retrieve the hashed password from the database
                hashed_password = user['admin_pass'].encode('utf-8')
                
                # Check if the provided password matches the hashed password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    
                    # update login attempt
                    FraudDetection().adminFraudDetection(user['admin_email'], True)
                    return True, user['admin_email']
                
                else:
                    isFraud, message = FraudDetection().adminFraudDetection(user['admin_email'], False)
                    print(f"Login attempt failed: {message}")

                    if not isFraud:
                        return False, message

                    return False,"Incorrect password"

        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            raise
    

    def getAdminTokenByEmail(self, email):

        connection = getDBConnection(current_app.config['ADMIN_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Query to retrieve the hashed password and status
                sql_query = '''
                    SELECT admin_secret_key
                    FROM Admin 
                    WHERE admin_email = %s
                '''
                cursor.execute(sql_query, (email,))
                user = cursor.fetchone()
                return user
            
        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            return False
        
    def update2FAbyEmail(self, email):
        connection = getDBConnection(current_app.config['ADMIN_SCHEMA'])
        try:
            with connection.cursor() as cursor:
                sql_query = '''
                    UPDATE Admin
                    SET admin_mfa_enabled = 1
                    WHERE admin_email = %s
                '''
                cursor.execute(sql_query, (email))
                connection.commit()
                return True
        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            return False
        