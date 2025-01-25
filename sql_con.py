import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host ="localhost",
        user="root",
        password="Kumar@#$123",
        database = "electricity_billing"
    )
    return conn
