import os
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "3000"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "12Sanjay@raj"),
            database=os.getenv("DB_NAME", "trading_db")
        )
        print("✅ Connected to MySQL database successfully")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        raise
