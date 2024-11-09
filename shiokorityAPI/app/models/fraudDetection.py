import pymysql
from ..auth.databaseConnection import getDBConnection
from flask import current_app
from decimal import Decimal

class FraudDetection():

    def __init__(self):
        # Configure detection thresholds
        self.thresholds = {
            'amount': 1000,                    # Single transaction amount
            'daily_total': 3000,               # Daily total amount
            'hourly_transactions': 5,          # Transactions per hour
            'daily_transactions': 10,          # Transactions per day
            'rapid_transaction': 3,            # Rapid transactions in 5 minutes
            'max_attempts': 5
        }

    def _check_amount(self, amount):
        """Check if single transaction amount is suspiciously high"""
        if amount > self.thresholds['amount']:
            return False, f"Transaction amount (${amount}) exceeds the limit of ${self.thresholds['amount']}. This transaction has been stopped for your security."
        return True, ""
    
    def _check_daily_total(self, user_id, new_amount):
        """Check if daily total spending is suspicious"""
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sqlQuery = """
                SELECT COALESCE(SUM(transaction_amount), 0) as total_spent
                FROM Transaction
                WHERE cust_id = %s
                AND DATE(transaction_date_created) = CURDATE();
                """

                cursor.execute(sqlQuery, (user_id))
                total_spent = cursor.fetchone()['total_spent']

                if total_spent + new_amount > self.thresholds['daily_total']:
                    return False, f"Daily spending limit of ${self.thresholds['daily_total']} exceeded. This transaction has been stopped for your security."
                
                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_daily_total: {e}")
            return False, "Transaction processing error. This transaction has been stopped."
        finally:
            connection.close()
    
    def _check_transaction_frequency(self, user_id):
        """Check hourly and daily transaction counts"""
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sqlQuery = """
                SELECT COUNT(*) as transactions_last_hour
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= DATE_SUB(NOW(), INTERVAL 1 HOUR);
                """

                cursor.execute(sqlQuery, (user_id))
                transactions_last_hour = cursor.fetchone()['transactions_last_hour']

                if transactions_last_hour >= self.thresholds['hourly_transactions']:
                    return False, f"Maximum transactions per hour ({self.thresholds['hourly_transactions']}) exceeded. This transaction has been stopped for your security."

                sqlQuery = """
                SELECT COUNT(*) as transactions_today
                FROM Transaction
                WHERE cust_id = %s
                AND DATE(transaction_date_created) = CURDATE();
                """
                
                cursor.execute(sqlQuery, (user_id))
                transactions_today = cursor.fetchone()['transactions_today']

                if transactions_today >= self.thresholds['daily_transactions']:
                    return False, f"Maximum daily transactions ({self.thresholds['daily_transactions']}) exceeded. This transaction has been stopped for your security."
                
                return True, ""
  
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_transaction_frequency: {e}")
            return False, "Transaction processing error. This transaction has been stopped."
        finally:
            connection.close()

    def _check_sudden_pattern_change(self, user_id, amount):
        """
        Check if transaction amount is significantly different from user's pattern
        Uses 200% of average as threshold - simpler and more intuitive
        """
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sqlQuery = """
                SELECT 
                    AVG(transaction_amount) as avg_amount,
                    MAX(transaction_amount) as max_amount  -- Added for reference
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= NOW() - INTERVAL 30 DAY
                """

                cursor.execute(sqlQuery, (user_id))
                result = cursor.fetchone()

                if result['avg_amount'] is None:
                    return True, ""

                # Flag if transaction is more than 200% of average
                if amount > (result['avg_amount'] * 2):
                    return False, f"Unusual transaction amount detected (${amount} exceeds typical pattern). This transaction has been stopped for your security."
                
                return True, ""
                
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_sudden_pattern_change: {e}")
            return False, "Transaction processing error. This transaction has been stopped."
        finally:
            connection.close()

    def _check_rapid_transactions(self, user_id, timestamp):
        """Check for suspiciously rapid consecutive transactions"""
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sqlQuery = """
                SELECT transaction_date_created
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= %s - INTERVAL 5 MINUTE
                ORDER BY transaction_date_created DESC
                """
                
                cursor.execute(sqlQuery, (user_id, timestamp))
                recent_transactions = cursor.fetchall()

                if len(recent_transactions) >= self.thresholds['rapid_transaction']:
                    return False, "Multiple rapid transactions detected. This transaction has been stopped for your security."
                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_rapid_transactions: {e}")
            return False, "Transaction processing error. This transaction has been stopped."
        finally:
            connection.close()

    def detect_transaction_fraud(self, user_id, amount, timestamp):
        """
        Main fraud detection method that runs all checks
        Returns: (is_safe, message)
        """
        amount = Decimal(amount).quantize(Decimal('0.00'))

        checks = [
            self._check_amount(amount),
            self._check_daily_total(user_id, amount),
            self._check_transaction_frequency(user_id),
            self._check_sudden_pattern_change(user_id, amount),
            self._check_rapid_transactions(user_id, timestamp)
        ]

        for is_safe, message in checks:
            if not is_safe:
                return False, f"Security Alert: {message}"

        return True, "Transaction authorized"
    
    def check_login_attempts(self, adminEmail):
        connection = getDBConnection(current_app.config['ADMIN_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                sqlQuery = """
                SELECT admin_login_flag_counter
                FROM Admin 
                WHERE admin_email = %s
                """
                cursor.execute(sqlQuery, (adminEmail))
                login_attempts = cursor.fetchone()['admin_login_flag_counter']

                if login_attempts >= self.thresholds['max_attempts']:
                    sqlQuery = """
                    UPDATE Admin
                    SET admin_login_flag_counter = 0,
                    admin_account_status = 0
                    WHERE admin_email = %s
                    """
                    cursor.execute(sqlQuery, (adminEmail))
                    connection.commit()
                    return False, "Account locked due to multiple failed login attempts. This login has been stopped for your security."
        
                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error check_login_attempts: {e}")
            return False, "Authentication error. This login has been stopped."
        
    def update_login_attempts(self, adminEmail, status):
        connection = getDBConnection(current_app.config['ADMIN_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                if status:
                    sqlQuery = """
                    UPDATE Admin
                    SET admin_login_flag_counter = 0
                    WHERE admin_email = %s
                    """
                else:
                    sqlQuery = """
                    UPDATE Admin
                    SET admin_login_flag_counter = admin_login_flag_counter + 1
                    WHERE admin_email = %s
                    """

                cursor.execute(sqlQuery, (adminEmail))
                connection.commit()

                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error update_login_attempts: {e}")
            return False, "Authentication error. This login has been stopped."
        finally:
            connection.close()

    def adminFraudDetection(self, adminEmail, status):
        """
        Main fraud detection method that runs all checks
        Returns: (is_safe, message)
        """
        checks = [
            self.check_login_attempts(adminEmail),
            self.update_login_attempts(adminEmail, status)
        ]

        for is_safe, message in checks:
            if not is_safe:
                return True, f"Security Alert: {message}"

        return False, "Authentication successful"