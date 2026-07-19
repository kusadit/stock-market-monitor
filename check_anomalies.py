import sqlite3

DB_PATH = "database/market_data.db"

# Trigger an alert if price changes by 5% or more
THRESHOLD_PERCENT = 5.0


def check_price_spikes():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all unique tickers
    tickers = cursor.execute(
        """
        SELECT DISTINCT ticker
        FROM stock_prices
        """
    ).fetchall()

    # Check each ticker individually
    for (ticker,) in tickers:

        # Get the latest two prices
        rows = cursor.execute(
            """
            SELECT price, fetched_at
            FROM stock_prices
            WHERE ticker = ?
            ORDER BY fetched_at DESC
            LIMIT 2
            """,
            (ticker,)
        ).fetchall()

        # Skip if there are fewer than 2 records
        if len(rows) < 2:
            print(f"Not enough data for {ticker}")
            continue

        latest_price = rows[0][0]
        previous_price = rows[1][0]

        # Calculate percentage change
        change_percent = abs(
            (latest_price - previous_price) / previous_price
        ) * 100

        print(f"\nTicker: {ticker}")
        print(f"Previous Price: {previous_price}")
        print(f"Latest Price: {latest_price}")
        print(f"Change: {change_percent:.2f}%")

        # Check if change exceeds threshold
        if change_percent >= THRESHOLD_PERCENT:

            cursor.execute(
                """
                INSERT INTO alerts (ticker, alert_type, message)
                VALUES (?, ?, ?)
                """,
                (
                    ticker,
                    "PRICE_SPIKE",
                    f"{change_percent:.2f}% price change detected"
                )
            )

            conn.commit()

            print("ALERT GENERATED!")

    conn.close()


if __name__ == "__main__":
    check_price_spikes()