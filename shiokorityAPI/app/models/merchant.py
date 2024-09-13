import pymysql
from flask import current_app, g
import bcrypt

class Merchant:
    @staticmethod
    def get_db_connection():
        if 'db' not in g:
            g.db = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database='merchant_management',  # Make sure the database name matches your schema
                cursorclass=pymysql.cursors.DictCursor
            )
        return g.db

    @staticmethod
    def create_merchant(merch_email, pass_hash, merch_name=None, merch_phone=None, merch_address=None):
        # Hash the password using bcrypt
        pass_hash = bcrypt.hashpw(pass_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Check if email already exists
        existing_merchant = Merchant.get_merchant_by_email(merch_email)
        if existing_merchant:
            return False, "Email already in use"

        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                # Insert the new merchant
                sql_query = """
                    INSERT INTO Merchant (merch_email, pass_hash, merch_name, merch_phone, merch_address, date_created, date_updated_on, status)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), 'active')
                """
                cursor.execute(sql_query, (merch_email, pass_hash, merch_name, merch_phone, merch_address))
                connection.commit()
                return True, "Merchant created successfully"

        except pymysql.MySQLError as e:
            print(f"Error creating merchant: {e}")
            return False, f"Error creating merchant: {e}"

    @staticmethod
    def get_all_merchants():
        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Merchant"
                cursor.execute(sql_query)
                merchants = cursor.fetchall()

                if not merchants:
                    return None  # No merchants found

                return merchants  # Merchants data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchants: {e}")
            return None  # Return None in case of an error

    @staticmethod
    def get_merchant_by_id(merchant_id):
        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Merchant WHERE merch_id = %s"
                cursor.execute(sql_query, (merchant_id,))
                merchant = cursor.fetchone()

                if not merchant:
                    return None  # No merchant found

                return merchant  # Merchant data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant: {e}")
            return None  # Return None in case of an error

    @staticmethod
    def get_merchant_by_email(merch_email):
        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Merchant WHERE merch_email = %s"
                cursor.execute(sql_query, (merch_email,))
                merchant = cursor.fetchone()

                return merchant  # Merchant data fetched successfully

        except pymysql.MySQLError as e:
            print(f"Error fetching merchant by email: {e}")
            return None

    @staticmethod
    def update_merchant_details(merch_id, merch_data):
        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                sql_query = """
                    UPDATE Merchant 
                    SET merch_name = %s, merch_phone = %s, merch_address = %s, date_updated_on = NOW()
                    WHERE merch_id = %s
                """
                affected_rows = cursor.execute(sql_query, (
                    merch_data.get('merch_name'),
                    merch_data.get('merch_phone'),
                    merch_data.get('merch_address'),
                    merch_id
                ))

                if affected_rows == 0:
                    return False  # No rows were affected, possibly invalid merchant ID

                connection.commit()
                return True

        except pymysql.MySQLError as e:
            print(f"Error updating merchant details: {e}")
            connection.rollback()
            return False

    @staticmethod
    def update_merchant_status(merch_id, status):
        try:
            connection = Merchant.get_db_connection()
            with connection.cursor() as cursor:
                sql_query = "UPDATE Merchant SET status = %s, date_updated_on = NOW() WHERE merch_id = %s"
                affected_rows = cursor.execute(sql_query, (status, merch_id))

                if affected_rows == 0:
                    return False  # No rows were affected, possibly invalid merchant ID

                connection.commit()
                return True

        except pymysql.MySQLError as e:
            print(f"Error updating merchant status: {e}")
            connection.rollback()
            return False

    @staticmethod
    def login(merch_email, pass_hash):
        try:
            merchant = Merchant.get_merchant_by_email(merch_email)
            if not merchant:
                return False, "Invalid email"

            # Verify the password using native bcrypt
            if not bcrypt.checkpw(pass_hash.encode('utf-8'), merchant['pass_hash'].encode('utf-8')):
                return False, "Invalid password"

            return True, merchant  # Login successful, return merchant data

        except pymysql.MySQLError as e:
            print(f"Error logging in: {e}")
            return False, "Error logging in"