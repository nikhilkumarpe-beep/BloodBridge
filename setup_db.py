import pymysql
import os

def create_database():
    try:
        # Connect to MySQL server (no database selected)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Nikhil@260405',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # Create database if it doesn't exist
                cursor.execute("CREATE DATABASE IF NOT EXISTS blood_donation_system")
                print("Database 'blood_donation_system' created or already exists.")
        finally:
            connection.close()
            
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
