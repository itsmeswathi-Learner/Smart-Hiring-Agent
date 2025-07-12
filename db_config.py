import MySQLdb
from MySQLdb import Error
import mysql.connector

def get_connection():
    try:
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="Swathi@04mysql",
            db="smart_hiring_db"
        )
        
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def fetch_all(query, params=None):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        print("Query executed and committed successfully!")
        return True
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        conn.close()
