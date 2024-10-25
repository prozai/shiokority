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
            'rapid_transaction': 3             # Rapid transactions in 5 minutes
        }

    def _check_amount(self, amount):
        """Check if single transaction amount is suspiciously high"""

        if amount > self.thresholds['amount']:
            return False, f"Amount ${amount} exceeds single transaction limit"
        return True, ""
    
    def _check_daily_total(self, user_id, new_amount):
        """Check if daily total spending is suspicious"""
        
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Fetch the total amount spent by the user today

                sqlQuery = """
                SELECT COALESCE(SUM(transaction_amount), 0) as total_spent
                FROM Transaction
                WHERE cust_id = %s
                AND DATE(transaction_date_created) = CURDATE();
                """

                cursor.execute(sqlQuery, (user_id))
                total_spent = cursor.fetchone()['total_spent']


                if total_spent + new_amount > self.thresholds['daily_total']:
                    return False, f"Daily total amount ${total_spent + new_amount} exceeds daily limit"
                
                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_daily_total: {e}")
            return False, "An error occurred"
        finally:
            connection.close()
    
    def _check_transaction_frequency(self, user_id):
        """Check hourly and daily transaction counts"""

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Fetch the number of transactions by the user in the last hour

                sqlQuery = """
                SELECT COUNT(*) as transactions_last_hour
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= DATE_SUB(NOW(), INTERVAL 1 HOUR);
                """

                cursor.execute(sqlQuery, (user_id))
                transactions_last_hour = cursor.fetchone()['transactions_last_hour']

                if transactions_last_hour > self.thresholds['hourly_transactions']:
                    return False, f"Hourly transaction limit exceeded"

                # Fetch the number of transactions by the user today

                sqlQuery = """
                SELECT COUNT(*) as transactions_today
                FROM Transaction
                WHERE cust_id = %s
                AND DATE(transaction_date_created) = CURDATE();
                """
                
                cursor.execute(sqlQuery, (user_id))
                transactions_today = cursor.fetchone()['transactions_today']

                if transactions_today > self.thresholds['daily_transactions']:
                    return False, f"Daily transaction limit exceeded"
                
                return True, ""
  
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_transaction_frequency: {e}")
            return False, "An error occurred"
        finally:
            connection.close()

    def _check_sudden_pattern_change(self, user_id, amount):
        """Check if transaction amount is significantly different from user's pattern"""

        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Fetch the average transaction amount by the user

                sqlQuery = """
                SELECT AVG(transaction_amount) as avg_amount, STDDEV(transaction_amount) as stddev
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= NOW() - INTERVAL 30 DAY
                """

                cursor.execute(sqlQuery, (user_id))
                result = cursor.fetchone()

                # If no history, skip this check
                if result['avg_amount'] == None or result['stddev'] == None:
                    return True, ""

                # Flag if amount is more than 3 standard deviations from mean
                if abs(amount - result['avg_amount']) > (3 * result['stddev']):
                    return False, f"Amount ${amount} significantly differs from usual pattern"
                return True, ""
            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_sudden_pattern_change: {e}")
            return False, "An error occurred"
        finally:
            connection.close()

    def _check_rapid_transactions(self, user_id, timestamp):
        """Check for suspiciously rapid consecutive transactions"""
        
        connection = getDBConnection(current_app.config['SHIOKORITY_API_SCHEMA'])

        try:
            with connection.cursor() as cursor:
                # Fetch the timestamp of the last transaction by the user

                sqlQuery = """
                SELECT transaction_date_created
                FROM Transaction
                WHERE cust_id = %s
                AND transaction_date_created >= %s - INTERVAL 5 MINUTE
                ORDER BY transaction_date_created DESC
                """
                
                cursor.execute(sqlQuery, (user_id, timestamp))
                recent_transactions = cursor.fetchall()

                if len(recent_transactions) >= self.thresholds['rapid_transaction']:  # More than 3 transactions in 5 minutes
                    return False, "Too many rapid transactions"
                return True, ""

            
        except pymysql.MySQLError as e:
            connection.rollback()
            print(f"Error _check_rapid_transactions: {e}")
            return False, "An error occurred"
        finally:
            connection.close()

    def detect_transaction_fraud(self, user_id, amount, timestamp):
        """
        Main fraud detection method that runs all checks
        Returns: (is_safe, message)
        """

        # Round amount to 2 decimal places
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
                return False, f"Fraud Alert: {message}"

        return True, "Transaction appears legitimate"