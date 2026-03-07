import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="serverless-eu-central-1.sysp0000.db1.skysql.com",
        port=4042,
        user="dbpwf34135244",
        password=os.getenv("DB_PASSWORD"),
        database="aykor_dev", 
        ssl_ca="skysql_ca.pem",
        ssl_verify_cert=True
    )
