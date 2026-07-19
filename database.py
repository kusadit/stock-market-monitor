import sqlite3

# Path to the SQLite database
DB_PATH = "database/market_data.db"


def create_database():
    # Connect to the database (creates it if it doesn't exist)
    connection = sqlite3.connect(DB_PATH)

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Create stock_prices table
    create_stock_prices_table = """
    CREATE TABLE IF NOT EXISTS stock_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        price REAL NOT NULL,
        volume INTEGER,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Create alerts table
    create_alerts_table = """
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        alert_type TEXT NOT NULL,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Execute both SQL queries
    cursor.execute(create_stock_prices_table)
    cursor.execute(create_alerts_table)

    # Save changes
    connection.commit()

    # Close the connection
    connection.close()

    print("Database setup completed successfully!")
    print("Tables created:")
    print("- stock_prices")
    print("- alerts")


create_database()