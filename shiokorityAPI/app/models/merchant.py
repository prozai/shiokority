import pymysql
from flask import current_app
import bcrypt
from ..auth.databaseConnection import getDBConnection

class Merchant:

    # 143
    def createMerchant(self, merchant):
        
        values = (merchant['name'], merchant['email'], merchant['phone'], merchant['address'], merchant['uen'])   

        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])

            with connection.cursor() as cursor:
                sqlQuery = """
                    INSERT INTO Merchant (merch_name, merch_email, merch_phone, merch_address, merch_pass, date_created, date_updated_on, merch_status, merch_uen)
                    VALUES (%s, %s, %s, %s, '$2y$10$IvuJ8FziVxYNbLIOMllv.Oou3GLwBe5RAlElZgZTY7cZH.xvLokPm', NOW(), NOW(), 1, %s)
                """
                with connection.cursor() as cursor:
                    cursor.execute(sqlQuery, values)
                    connection.commit()
                return True  # Merchant created successfully

        except pymysql.MySQLError as e:
            print(f"Error creating merchant: {e}")
            return False  # Return False in case of an error

    # 144
    def getMerchantData(self):
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sqlQuery = "SELECT * FROM Merchant WHERE merch_status = 1"
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

            connection = getDBConnection(current_app.config['PAY_SCHEMA'])

            with connection.cursor() as cursor:
                sqlQuery = "SELECT * FROM Merchant WHERE merch_id = %s"
                cursor.execute(sqlQuery, (id,))
                merchant = cursor.fetchone()

                if merchant is None:
                    return False

                return merchant  # Merchant fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant: {e}")
            return False  # Return False in case of an error

    # 146
    def updateMerchantDetails(self, merchID,merchData):
        connection = getDBConnection(current_app.config['PAY_SCHEMA'])
        try:
            query = """UPDATE Merchant 
                    SET merch_name = %s, merch_email = %s, merch_phone = %s, date_updated_on = NOW(), merch_uen = %s, merch_address = %s
                    WHERE merch_id = %s"""
            with connection.cursor() as cursor:
                affected_rows = cursor.execute(query, (merchData['merch_name'], merchData['merch_email'], merchData['merch_phone'],merchData['merch_uen'], merchData['merch_address'], merchID))
                connection.commit()

            if affected_rows == 0:
                return False  # No rows were affected

            return True

        except Exception as e:
            connection.rollback()
            print(f"Error updating merchant details: {e}")
            return False

    def updateMerchantStatus(self, merch_id, status):

        connect = getDBConnection(current_app.config['PAY_SCHEMA'])
        try:
            with connect.cursor() as cursor:
                new_status = bool(int(status))  # Convert status to boolean
                sql = "UPDATE Merchant SET merch_status = %s, date_updated_on = NOW() WHERE merch_id = %s"

                validate = cursor.execute(sql, (new_status, merch_id))

                if validate == 0:
                    return False  # No rows affected
            
            connect.commit()
            return True

        except Exception as e:
            print(f"Error updating merchant status: {str(e)}")
            connect.rollback()
            return False
        finally:
            connect.close()

    # 130
    def registerMerchant(self, merchant):

        hash_pass = bcrypt.hashpw(merchant['merch_pass'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        existing_merchant = self.getMerchantByEmail(merchant['merch_email'])

        if existing_merchant:
            return False, "Email already in use"

        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    INSERT INTO Merchant (merch_name, merch_email, merch_phone, merch_address, merch_pass, date_created, date_updated_on, merch_status, merch_uen)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), 1, %s)
                """

                cursor.execute(sql_query, (merchant['merch_name'], merchant['merch_email'], merchant['merch_phone'], merchant['merch_address'], hash_pass, merchant['uen']))

                connection.commit()
                return True, "Merchant created successfully"

        except pymysql.MySQLError as e:
            print(f"Error creating merchant: {e}")
            return False, f"Error creating merchant: {e}"

    # 131
    def login(self, merch_email, merch_pass):
        # Login function using bcrypt
        try:
            merchant = self.getMerchantByEmail(merch_email)
            if not merchant:
                return False, "Invalid email"

            if not bcrypt.checkpw(merch_pass.encode('utf-8'), merchant['merch_pass'].encode('utf-8')):
                return False, "Invalid password"

            return True, merchant  # Login successful, return merchant data

        except pymysql.MySQLError as e:
            print(f"Error logging in: {e}")
            return False, "Error logging in"

    def getMerchantByEmail(self, merch_email):
        # Fetch merchant by email - used in login and create
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Merchant WHERE merch_email = %s"
                cursor.execute(sql_query, (merch_email,))
                merchant = cursor.fetchone()  
                return merchant  # Merchant data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant by email: {e}")
            return False

    def getMerchantByID(self, merch_id):
        # Fetch merchant by ID from the database
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT merch_id, merch_name, merch_email, merch_phone, merch_address, merch_uen 
                    FROM Merchant 
                    WHERE merch_id = %s
                """
                cursor.execute(sql_query, (merch_id,))
                merchant = cursor.fetchone()

                if not merchant:
                    return None  # No merchant found

                return merchant  # Merchant data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant: {e}")
            return None
    
    def validateTokenEmail(self, email):
        # Validate token email
        try:
            connection = getDBConnection(current_app.config['PAY_SCHEMA'])
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Merchant WHERE merch_email = %s and merch_status = 1"
                cursor.execute(sql_query, (email,))
                merchant = cursor.fetchone()

                if not merchant:
                    return False  # No merchant found

                return True  # Merchant found

        except pymysql.MySQLError as e:
            print(f"Error validating token email: {e}")
            return False