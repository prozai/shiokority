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
                database=current_app.config['USER_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connection:
                with connection.cursor() as cursor:
                    # Query to retrieve the hashed password and status
                    sql_query = '''
                        SELECT admin_id, admin_email, pass_hash, status 
                        FROM Admin 
                        WHERE admin_email = %s
                    '''
                    cursor.execute(sql_query, (email,))
                    user = cursor.fetchone()
                    
                    
                    if not user:
                        print(f"Login attempt failed: User not found for email {email}")
                        return False
                    
                    if user['status'] != 1:
                        print(f"Login attempt failed: Inactive account for email {email}")
                        return False
                    
                    # Retrieve the hashed password from the database
                    hashed_password = user['pass_hash'].encode('utf-8')
                    
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
    def addUser(self, email, password, first_name, last_name, status):
        connection = None
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['USER_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Hash the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            with connection.cursor() as cursor:
                # Insert the new user into the Admin table
                sql_query = '''
                    INSERT INTO User_Profile (user_email, pass_hash, first_name, last_name, status, date_created, date_updated_on)
                    VALUES (%s, %s, %s, %s, %s, NOW(),NOW())
                '''
                cursor.execute(sql_query, (email, hashed_password, first_name, last_name, status))
                connection.commit()
                
                # Return the new user ID
                return cursor.lastrowid

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
                database=current_app.config['USER_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            ) as connect:
                with connect.cursor() as cursor:
                    sqlQuery = "SELECT * FROM User_Profile"
                    cursor.execute(sqlQuery)
                    users = cursor.fetchall()
                
                if not users:
                    return []

                return users
        except pymysql.MySQLError as e:
            print(f"Error fetching users: {e}")
            return []


    #141
    #138
    def update_user(self, user_id, email=None, first_name=None, last_name=None, status=None):
        try:
            # Establish a connection to the database
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['USER_SCHEMA'],
                cursorclass=pymysql.cursors.DictCursor
            )

            # Construct SQL query based on provided fields
            updates = []
            params = []

            if email:
                updates.append("user_email = %s")
                params.append(email)

            if first_name:
                updates.append("first_name = %s")
                params.append(first_name)

            if last_name:
                updates.append("last_name = %s")
                params.append(last_name)

            if status is not None:
                updates.append("status = %s")
                params.append(status)

            # Ensure there are fields to update
            if not updates:
                return False

            # Add the `date_updated_on` field
            updates.append("date_updated_on = NOW()")

            params.append(user_id)

            # Prepare the SQL query
            sql_query = f"UPDATE User_Profile SET {', '.join(updates)} WHERE user_id = %s"

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
