import sqlite3
import yfinance as yf

from logger_config import logger

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
        logger.info(f"Fetching data for {ticker}")

        stock = yf.Ticker(ticker)

        data = stock.history(period="1d")

        if data.empty:
            logger.warning(f"No data found for {ticker}")

            log_alert(
                conn,
                ticker,
                "MISSING_DATA",
                "No data returned from Yahoo Finance"
            )
            return

        price = float(data["Close"].iloc[-1])
        volume = int(data["Volume"].iloc[-1])

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO stock_prices (ticker, price, volume)
            VALUES (?, ?, ?)
            """,
            (ticker, price, volume)
        )

        conn.commit()

        logger.info(
            f"{ticker} | Price: {price} | Volume: {volume} | Saved Successfully"
        )

    except Exception as e:

        logger.error(f"Error fetching {ticker}: {e}")

        log_alert(
            conn,
            ticker,
            "API_FAILURE",
            str(e)
        )


if __name__ == "__main__":

    logger.info("========== Fetch Data Pipeline Started ==========")

    connection = get_connection()

    for ticker in TICKERS:
        fetch_and_store(ticker, connection)

    connection.close()

    logger.info("========== Fetch Data Pipeline Completed ==========")