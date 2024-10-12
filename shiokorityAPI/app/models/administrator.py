import pymysql
from flask import current_app
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
                database=current_app.config['ADMIN_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
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
                        return False
                    
                    if user['admin_account_status'] != 1:
                        print(f"Login attempt failed: Inactive account for email {email}")
                        return False
                    
                    # Retrieve the hashed password from the database
                    hashed_password = user['admin_pass'].encode('utf-8')
                    
                    # Check if the provided password matches the hashed password
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
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
    
    
    # My work of art
    #136
    def addUser(self, user):
        connection = None
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Hash the password before storing
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            with connection.cursor() as cursor:
                # Insert the new user into the Admin table
                sql_query = '''
                    INSERT INTO Customer (cust_email, cust_pass, cust_fname, cust_lname, cust_status, cust_address, cust_phone, date_created, date_updated_on)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(),NOW())
                '''
                cursor.execute(sql_query, (user['email'], hashed_password, user['first_name'], user['last_name'], user['status'], user['address'], user['phone']))
                connection.commit()
                return True

        except MySQLError as e:
            print(f"Database error during user creation: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during user creation: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()  # Ensure the connection is closed after the operation

    #137
    def get_all_users(self):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connect:
                with connect.cursor() as cursor:
                    sqlQuery = "SELECT * FROM Customer"
                    cursor.execute(sqlQuery)
                    users = cursor.fetchall()
                if not users:
                    return False
                return users
        except pymysql.MySQLError as e:
            print(f"Error fetching users: {e}")
            return False

    def getUserById(self, user_id):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve user details by user_id
                    sql_query = '''
                        SELECT cust_id, cust_email, cust_fname, cust_lname, cust_status, cust_address, cust_phone, date_created, date_updated_on
                        FROM Customer
                        WHERE cust_id = %s
                    '''
                    cursor.execute(sql_query, (user_id,))
                    user = cursor.fetchone()
                    
                    # Return the user data if found, otherwise None
                    if user:
                        return user
                    else:
                        return False
        except MySQLError as e:
            print(f"Database error during user retrieval: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error during user retrieval: {str(e)}")
            return False

    #141
    #138
    def update_user(self, cust_id, email=None, first_name=None, last_name=None, address=None, phone=None, status=None):
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['PAY_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Construct SQL query based on provided fields
            updates = []
            params = []

            if email:
                updates.append("cust_email = %s")
                params.append(email)

            if first_name:
                updates.append("cust_fname = %s")
                params.append(first_name)

            if last_name:
                updates.append("cust_lname = %s")
                params.append(last_name)

            if address:
                updates.append("cust_address = %s")
                params.append(address)

            if phone:
                updates.append("cust_phone = %s")
                params.append(phone)

            if status is not None:
                updates.append("cust_status = %s")
                params.append(status)

            # Ensure there are fields to update
            if not updates:
                return False

            # Add the `date_updated_on` field
            updates.append("date_updated_on = NOW()")

            params.append(cust_id)

            # Prepare the SQL query
            sql_query = f"UPDATE Customer SET {', '.join(updates)} WHERE cust_id = %s"

            with connection.cursor() as cursor:
                # Execute the query with the provided params
                cursor.execute(sql_query, params)
                connection.commit()
                return cursor.rowcount > 0  # Return True if any row was updated

        except MySQLError as e:
            print(f"Database error during user update: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during user update: {str(e)}")
            return False

        finally:
            if connection:
                connection.close()

    def getAdminTokenByEmail(self, email):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['ADMIN_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
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

        except MySQLError as e:
            print(f"Database error during login validation: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            return False
        
    def update2FAbyEmail(self, email):
        try:
            with pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['ADMIN_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    sql_query = '''
                        UPDATE Admin
                        SET admin_mfa_enabled = 1
                        WHERE admin_email = %s
                    '''
                    cursor.execute(sql_query, (email))
                    connection.commit()
                    return True
        except MySQLError as e:
            print(f"Database error during login validation: {str(e)}")
            return False

        except Exception as e:
            print(f"Unexpected error during login validation: {str(e)}")
            return False