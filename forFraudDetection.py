from shiokorityAPI.config import config
import pymysql
from datetime import datetime, timedelta
import random

envConfig = config['development']

def getDBConnection(schema_name):

    configuration = {
        'host': envConfig.MYSQL_HOST,
        'user': envConfig.MYSQL_USER,
        'password': envConfig.MYSQL_PASSWORD,
        'database': schema_name,
        'cursorclass': pymysql.cursors.DictCursor
    }
    # Create the connection
    connection = pymysql.connect(**configuration)

    # Set timezone for this connection
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+08:00'")
        connection.commit()

    return connection


def insertHourlyFraudTransaction(custId):
    connection = getDBConnection(envConfig.SHIOKORITY_API_SCHEMA)
    try:
        with connection.cursor() as cursor:
            # Calculate timestamp 5 minutes ago
            timestamp = datetime.now() - timedelta(minutes=5)
            
            sql = """
            INSERT INTO Transaction (
                transaction_amount, 
                transaction_status, 
                transaction_date_created,
                transaction_updated_on,
                cust_id,
                uen
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                100,
                'payment',
                timestamp,
                timestamp,  # Using same timestamp for update_on
                custId,
                '53339185K'
            ))
        connection.commit()
    except Exception as e:
        print(f"Error creating test transaction: {e}")
        connection.rollback()
    finally:
        connection.close()

def dayFraudTransaction(custId):
    """
    Insert fraud transactions for today only, starting from midnight
    """
    connection = getDBConnection(envConfig.SHIOKORITY_API_SCHEMA)
    try:
        with connection.cursor() as cursor:
            # Get today's date at midnight
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate current hour to ensure we only create transactions up to now
            current_hour = datetime.now().hour
            
            sql = """
            INSERT INTO Transaction (
                transaction_amount, 
                transaction_status, 
                transaction_date_created,
                transaction_updated_on,
                cust_id,
                uen
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Create timestamp for 5 hours ago from current time
            current_time = datetime.now()
            timestamp = current_time - timedelta(hours=5)
            
            # Ensure timestamp is still from today
            if timestamp.date() < today.date():
                timestamp = today + timedelta(hours=1)  # Start from 1 AM today if 5 hours ago would be yesterday
            
            # Generate a random transaction amount between 50 and 500
            amount = random.randint(100, 150)
            
            cursor.execute(sql, (
                amount,
                'payment',
                timestamp,
                timestamp,
                custId,
                '53339185K'
            ))
                
            connection.commit()
            print(f"Successfully inserted transaction for customer {custId} at {timestamp}")
            
    except Exception as e:
        print(f"Error creating daily transactions: {e}")
        connection.rollback()
    finally:
        connection.close()

def dayHourlyFraudTransaction(custId):

    connection = getDBConnection('shiokority_api')
    try:
        with connection.cursor() as cursor:
            # Get current date at midnight
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Create transactions for each hour
            for hour in range(10):
                # Create timestamp for this hour
                timestamp = today + timedelta(hours=hour)

                # Add a random number of minutes (0-59) for more realistic timing
                random_minutes = random.randint(0, 59)
                timestamp = timestamp + timedelta(minutes=random_minutes)

                sql = """
                INSERT INTO Transaction (
                    transaction_amount, 
                    transaction_status, 
                    transaction_date_created,
                    transaction_updated_on,
                    cust_id,
                    uen
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """

                # Generate a random transaction amount between 50 and 500
                amount = random.randint(100, 150)

                cursor.execute(sql, (
                    amount,
                    'payment',
                    timestamp,
                    timestamp,
                    custId,
                    '53339185K'
                ))

            connection.commit()

    except Exception as e:
        print(f"Error creating daily transactions: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    # for i in range(0,5):
    #     insertHourlyFraudTransaction(1)

    dayHourlyFraudTransaction(1)
    
    