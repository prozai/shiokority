from config import config
import pymysql

def getDBConnection(schema_name):
    configuration = {
        'host': config['development'].MYSQL_HOST,
        'user': config['development'].MYSQL_USER,
        'password': config['development'].MYSQL_PASSWORD,
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