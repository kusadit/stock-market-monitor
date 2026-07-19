import sqlite3
import yfinance as yf

# Database path
DB_PATH = "database/market_data.db"

# Stocks to monitor
TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def log_alert(conn, ticker, alert_type, message):
    """
    Stores an alert in the alerts table.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (ticker, alert_type, message)
        VALUES (?, ?, ?)
        """,
        (ticker, alert_type, message)
    )

    conn.commit()


def fetch_and_store(ticker, conn):
    """
    Fetches stock data from Yahoo Finance
    and stores it in the database.
    """

    try:
        print(f"\nFetching data for {ticker}...")

        # Create stock object
        stock = yf.Ticker(ticker)

        # Fetch today's data
        data = stock.history(period="1d")

        # Check if data exists
        if data.empty:
            log_alert(
                conn,
                ticker,
                "MISSING_DATA",
                "No data returned from Yahoo Finance"
            )
            print("No data found.")
            return

        # Extract required fields
        price = float(data["Close"].iloc[-1])
        volume = int(data["Volume"].iloc[-1])

        # Insert into database
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO stock_prices (ticker, price, volume)
            VALUES (?, ?, ?)
            """,
            (ticker, price, volume)
        )

        conn.commit()

        print(f"Price : {price}")
        print(f"Volume: {volume}")
        print("Data saved successfully!")

    except Exception as e:
        log_alert(
            conn,
            ticker,
            "API_FAILURE",
            str(e)
        )

        print(f"Error fetching {ticker}: {e}")


if __name__ == "__main__":

    connection = get_connection()

    for ticker in TICKERS:
        fetch_and_store(ticker, connection)

    connection.close()

    print("\nPipeline completed successfully!")