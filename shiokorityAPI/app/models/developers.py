import pymysql
from flask import current_app
import bcrypt

class Developers():
    
    def registerDeveloper(self, developer, secret_key):
        try:
            with pymysql.connect(host=current_app.config['MYSQL_HOST'], user=current_app.config['MYSQL_USER'],
                                 password=current_app.config['MYSQL_PASSWORD'], database=current_app.config['DEV_SCHEMA'],
                                 cursorclass=pymysql.cursors.DictCursor) as connect:

                with connect.cursor() as cursor:

                    # Check if the email already exists
                    cursor.execute("SELECT COUNT(*) as count FROM Developer WHERE dev_email = %s", (developer['email'],))
                    result = cursor.fetchone()
                    
                    if result['count'] > 0:
                        print("Error creating developers: Email already exists")
                        return False  # Email already exists

                    hashed_password = bcrypt.hashpw(developer['password'].encode('utf-8'), bcrypt.gensalt())

                    cursor.callproc('CreateDeveloper', (
                    developer['firstName'],
                    developer['lastName'],
                    developer['email'],
                    hashed_password,
                    developer['address'],
                    developer['phoneNumber'],
                    True,
                    secret_key
                ))
                    connect.commit()

                return True  # developers created successfully

        except pymysql.MySQLError as e:
            print(f"Error creating developers: {e}")
            return False  # Return False in case of an error
        
        
    def loginDeveloper(self, developer):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['DEV_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve the hashed password and status
                    sql_query = '''
                        SELECT developer_id, dev_email, hashed_password, status, twoFactorEnabled FROM Developer WHERE dev_email = %s
                    '''
                    cursor.execute(sql_query, (developer['email'],))
                    user = cursor.fetchone()
                    
                    if not user:
                        print(f"Login attempt failed: User not found for email {developer['email']}")
                        return False
                    
                    if user['status'] != 1:
                        print(f"Login attempt failed: Inactive account for email {developer['email']}")
                        return False
                    
                    # Retrieve the hashed password from the database
                    hashed_password = user['hashed_password'].encode('utf-8')
                    
                    # Check if the provided password matches the hashed password
                    if bcrypt.checkpw(developer['password'].encode('utf-8'), hashed_password):
                        return {"success" : True, "two_factor_enabled" : user['twoFactorEnabled']}
                    
                    else:
                        print(f"Login attempt failed: Incorrect password for email {developer['email']}")
                        return {"success" : False }
                        

        except pymysql.MySQLError as e:
            print(f"Database error during login validation: {str(e)}")
            raise

        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            raise
    
    def getDeveloperByEmail(self, email):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['DEV_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    sql_query = '''
                        SELECT *
                        FROM Developer
                        WHERE dev_email = %s
                    '''
                    cursor.execute(sql_query, (email,))
                    developer = cursor.fetchone()
                    
                    if developer is None:
                        print(f"Developer with email {email} not found")
                        return False
                    
                    return developer

        except pymysql.MySQLError as e:
            print(f"Database error fetching developer by email: {str(e)}")
            raise

        except Exception as e:
            print(f"Unexpected error fetching developer by email: {str(e)}")
            raise

    def update2FAbyEmail(self, email):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['DEV_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    sql_query = '''
                        UPDATE Developer
                        SET dev_mfa_enabled = 1
                        WHERE dev_email = %s
                    '''
                    cursor.execute(sql_query, (email))
                    connection.commit()
                    return True

        except pymysql.MySQLError as e:
            print(f"Database error updating 2FA status: {str(e)}")
            raise

        except Exception as e:
            print(f"Unexpected error updating 2FA status: {str(e)}")
            raise