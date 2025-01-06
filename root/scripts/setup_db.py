import mysql.connector
from mysql.connector import Error
from src.config.settings import DB_CONFIG

def create_database():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        
        # Create tables
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Active symbols table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_symbols (
            symbol VARCHAR(45) NOT NULL,
            name VARCHAR(255) NULL,
            exchange VARCHAR(255) NULL,
            asset_type VARCHAR(255) NULL,
            ipo_date DATE NULL,
            delisting_date DATE NULL,
            status VARCHAR(45) NULL,
            PRIMARY KEY (symbol),
            UNIQUE INDEX symbol_UNIQUE (symbol ASC)
        ) ENGINE=InnoDB;
        """)
        
        # Add other table creation statements here...
        
        connection.commit()
        print("Database setup completed successfully")
        
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
