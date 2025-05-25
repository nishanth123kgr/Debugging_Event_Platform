#!/usr/bin/env python3
"""
Direct SQL execution script for creating tables
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

def create_tables():
    """Create tables directly using SQL commands"""
    print("Creating database tables...")
    print("-" * 50)
    
    # SQL commands to create tables
    tables = {
        'q1': """
        CREATE TABLE IF NOT EXISTS `q1` (
            `id` varchar(50) NOT NULL,
            `submitted_time` longtext NOT NULL,
            `time_taken` longtext NOT NULL,
            `score` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """,
        'q2': """
        CREATE TABLE IF NOT EXISTS `q2` (
            `id` varchar(50) NOT NULL,
            `submitted_time` longtext NOT NULL,
            `time_taken` longtext NOT NULL,
            `score` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """,
        'q3': """
        CREATE TABLE IF NOT EXISTS `q3` (
            `id` varchar(50) NOT NULL,
            `submitted_time` longtext NOT NULL,
            `time_taken` longtext NOT NULL,
            `score` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """,
        'q4': """
        CREATE TABLE IF NOT EXISTS `q4` (
            `id` varchar(50) NOT NULL,
            `submitted_time` longtext NOT NULL,
            `time_taken` longtext NOT NULL,
            `score` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """,
        'q5': """
        CREATE TABLE IF NOT EXISTS `q5` (
            `id` varchar(50) NOT NULL,
            `submitted_time` longtext NOT NULL,
            `time_taken` longtext NOT NULL,
            `score` int(11) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """,
        'users': """
        CREATE TABLE IF NOT EXISTS `users` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `username` varchar(50) NOT NULL,
            `lang` varchar(8) NOT NULL,
            `name` varchar(50) DEFAULT NULL,
            `phone` varchar(15) NOT NULL,
            `q1_status` int(11) NOT NULL DEFAULT 0,
            `q2_status` int(11) NOT NULL DEFAULT 0,
            `q3_status` int(11) NOT NULL DEFAULT 0,
            `q4_status` int(11) NOT NULL DEFAULT 0,
            `q5_status` int(11) NOT NULL DEFAULT 0,
            `total_score` int(11) NOT NULL DEFAULT 0,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
    }
    
    try:
        # Connect to database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        print(f"Connected to database: {db_config['database']}")
        
        # Create each table
        for table_name, create_sql in tables.items():
            try:
                print(f"Creating table: {table_name}")
                cursor.execute(create_sql)
                print(f"  ✅ Table '{table_name}' created successfully")
            except mysql.connector.Error as err:
                print(f"  ❌ Error creating table '{table_name}': {err}")
        
        # Commit the changes
        connection.commit()
        
        # Verify tables were created
        print("\nVerifying tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Total tables in database: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        connection.close()
        
        print("\n✅ Database setup completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    create_tables()
