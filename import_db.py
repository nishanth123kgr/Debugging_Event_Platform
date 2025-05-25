#!/usr/bin/env python3
"""
Database schema import script
Imports the debugging.sql file into your Clever Cloud database
"""

import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def import_sql_file(sql_file_path):
    """Import SQL file into the database"""
    print(f"Importing SQL file: {sql_file_path}")
    print("-" * 50)
    
    try:
        # Read the SQL file
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Connect to database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Split SQL commands by semicolon and execute each
        sql_commands = sql_content.split(';')
        
        executed_commands = 0
        for command in sql_commands:
            command = command.strip()
            if command and not command.startswith('--') and not command.startswith('/*'):
                try:
                    cursor.execute(command)
                    executed_commands += 1
                except mysql.connector.Error as err:
                    # Skip some common errors that are not critical
                    if "already exists" in str(err).lower():
                        print(f"  Skipping: {err}")
                        continue
                    elif "unknown database" in str(err).lower():
                        print(f"  Skipping database creation: {err}")
                        continue
                    else:
                        print(f"  Warning: {err}")
                        continue
        
        # Commit the changes
        connection.commit()
        
        print(f"✅ Successfully executed {executed_commands} SQL commands")
        
        # Verify the import by checking tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Tables created: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        connection.close()
        
        print("✅ Database schema imported successfully!")
        
    except FileNotFoundError:
        print(f"❌ SQL file not found: {sql_file_path}")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    sql_file = "debugging.sql"
    import_sql_file(sql_file)
