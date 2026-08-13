"""
Quick Database Checker
Run this to see what data is stored in your MySQL database
"""

import mysql.connector

def check_database():
    try:
        # Connect to database using your credentials
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nikhil@260405',
            database='blood_donation_system'
        )
        cursor = conn.cursor()
        
        print("=" * 60)
        print("DATABASE CONNECTION SUCCESSFUL!")
        print("=" * 60)
        
        # List all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n📊 TABLES IN DATABASE:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "=" * 60)
        
        # Check each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            print(f"\n📋 Table: {table_name}")
            print(f"   Records: {count}")
            
            if count > 0:
                # Show first 5 records
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [col[0] for col in cursor.fetchall()]
                
                print(f"   Columns: {', '.join(columns)}")
                print(f"   Sample Data (first {min(count, 5)} records):")
                
                for i, row in enumerate(rows, 1):
                    print(f"   {i}. {row}")
            else:
                print("   ⚠️  No data in this table")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE CHECK COMPLETE!")
        print("=" * 60)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ ERROR: {err}")
        print("\nPossible issues:")
        print("1. MySQL server is not running")
        print("2. Database 'blood_donation_system' doesn't exist")
        print("3. Wrong username/password")
        print("4. MySQL not installed")

if __name__ == "__main__":
    check_database()
