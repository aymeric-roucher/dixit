import json
import psycopg2
import os

def open_sql_connection():
    password_railway = os.getenv('PGPASSWORD')
    conn = psycopg2.connect(
        database="railway",
        user="postgres",
        password=password_railway,
        host="containers-us-west-127.railway.app",
        port="5800",
    )
    conn.autocommit = True
    return conn
