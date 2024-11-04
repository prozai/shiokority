import pymysql
from flask import current_app
import logging
from datetime import datetime

# Set up the logger
logger = logging.getLogger(__name__)

class AuditTrail:
    def get_connection(self):
        """
        Establishes a database connection using the current app context configuration.

        Returns:
            pymysql.Connection: Connection object for interacting with the database.
        """
        return pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['SECURITY_SCHEMA'],
            cursorclass=pymysql.cursors.DictCursor
        )

    def log_entry(self, method, module, description):
        """
        Inserts a log entry into the Audit_Trail table.

        Parameters:
            method (str): The HTTP method used (e.g., 'POST', 'GET').
            module (str): The endpoint/module being accessed (e.g., '/create-merchant').
            description (str): Details about the action.

        Returns:
            bool: True if the entry was successfully logged, False otherwise.
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO Audit_Trail (audit_trail_method, audit_trail_module, audit_trail_description, timestamp)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (method, module, description, timestamp))
                    connection.commit()
                    return True
        except pymysql.MySQLError as e:
            logger.error(f"Database error logging audit trail entry: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error logging audit trail entry: {e}")
            return False

    def get_all_logs(self):
        """
        Fetches entries from the Audit_Trail table limited to the past month.

        Returns:
            list: A list of audit trail entries from the last month.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT * 
                    FROM Audit_Trail 
                    WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    ORDER BY audit_trail_id DESC
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return [dict(row) for row in result]
        except pymysql.MySQLError as e:
            logger.error(f"Database error fetching audit logs: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching audit logs: {e}")
            return []

    def get_logs_by_module(self, module):
        """
        Fetches entries from the Audit_Trail table for a specific module.

        Parameters:
            module (str): The module name to filter logs by.

        Returns:
            list: A list of audit trail entries filtered by module.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT * FROM Audit_Trail 
                    WHERE audit_trail_module = %s 
                    ORDER BY audit_trail_id DESC
                    """
                    cursor.execute(query, (module,))
                    result = cursor.fetchall()
                    return [dict(row) for row in result]
        except pymysql.MySQLError as e:
            logger.error(f"Database error fetching logs for module '{module}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching logs for module '{module}': {e}")
            return []

    def get_log_by_id(self, audit_id):
        """
        Fetches a single entry from the Audit_Trail table based on the audit trail ID.

        Parameters:
            audit_id (int): The ID of the audit trail entry to fetch.

        Returns:
            dict: The audit trail entry matching the ID, or None if not found.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT * FROM Audit_Trail 
                    WHERE audit_trail_id = %s
                    """
                    cursor.execute(query, (audit_id,))
                    result = cursor.fetchone()
                    return dict(result) if result else None
        except pymysql.MySQLError as e:
            logger.error(f"Database error fetching log with ID {audit_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching log with ID {audit_id}: {e}")
            return None
