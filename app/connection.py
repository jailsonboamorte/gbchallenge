import os

import mysql.connector as msql
from mysql.connector import Error


def get_connection():
    try:
        conn = msql.connect(
            host="mydb",
            user=os.environ["MYSQL_USER"],
            database=os.environ["MYSQL_DATABASE"],
            password=os.environ["MYSQL_PASSWORD"],
            port=3306,
        )

        return conn
    except Error as e:
        print("Error while connecting to MySQL", e)


def get_cursor(conn):
    if conn.is_connected():
        cursor = conn.cursor()
        return cursor
    return None
