from flask import current_app
import pymysql

def getDBConnection(schema_name):
        config = {
        'host': current_app.config['MYSQL_HOST'],
        'user': current_app.config['MYSQL_USER'],
        'password': current_app.config['MYSQL_PASSWORD'],
        'database': schema_name,
        'cursorclass': pymysql.cursors.DictCursor
    }
        return pymysql.connect(**config)