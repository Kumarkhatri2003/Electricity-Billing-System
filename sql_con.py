import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host ="localhost",
        user="root",
        password="Your_password",
        database = "electricity_billing"
    )
    return conn
