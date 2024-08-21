import pymysql
from flask import current_app
import bcrypt

class Administrator():
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    # 227
    def validateLogin(self):
        connect = pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'], password=current_app.config['MYSQL_PASSWORD'], database='usermanagement',
                                  cursorclass=pymysql.cursors.DictCursor)
        with connect.cursor() as cursor:
            # Query to retrieve the hashed password and status
            sqlQuery = 'SELECT admin_id, admin_username, pass_hash, status FROM admin WHERE admin_username = %s'
            cursor.execute(sqlQuery, (self.email,))
            user = cursor.fetchone()
            
            if user and user['status'] == 'active':
                # Retrieve the hashed password from the database
                hashed_password = user['pass_hash'].encode('utf-8')
                
                # Check if the provided password matches the hashed password
                if bcrypt.checkpw(self.password.encode('utf-8'), hashed_password):
                    print("Validation successful. User authenticated.")
                    return user
                else:
                    print("Invalid password.")
                    return False
            else:
                print("User not found or inactive.")
                return False
            
        