#!/usr/bin/env python3
"""
Database connection test script
Run this to verify your database configuration works
"""

import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'debugging'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    print(f"Host: {db_config['host']}")
    print(f"User: {db_config['user']}")
    print(f"Database: {db_config['database']}")
    print(f"Port: {db_config['port']}")
    print("-" * 40)
    
    try:
        # Attempt connection
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            
            # Get database info
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"Connected to database: {database_name[0]}")
            
            # Test basic query
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"Tables found: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
                
            cursor.close()
            
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed!")
        print(f"Error: {err}")
        
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("  → Check username and password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("  → Database does not exist")
        else:
            print(f"  → Error code: {err.errno}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    test_connection()
