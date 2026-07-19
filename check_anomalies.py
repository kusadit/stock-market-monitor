import sqlite3

from logger_config import logger

DB_PATH = "database/market_data.db"

# Trigger an alert if price changes by 5% or more
THRESHOLD_PERCENT = 5.0


def check_price_spikes():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    logger.info("========== Anomaly Detection Started ==========")

    tickers = cursor.execute(
        """
        SELECT DISTINCT ticker
        FROM stock_prices
        """
    ).fetchall()

    for (ticker,) in tickers:

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

        if len(rows) < 2:
            logger.warning(f"Not enough data to compare prices for {ticker}")
            continue

        latest_price = rows[0][0]
        previous_price = rows[1][0]

        change_percent = abs(
            (latest_price - previous_price) / previous_price
        ) * 100

        logger.info(
            f"{ticker} | Previous: {previous_price} | Latest: {latest_price} | Change: {change_percent:.2f}%"
        )

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

            logger.warning(
                f"PRICE SPIKE detected for {ticker} ({change_percent:.2f}%)"
            )

    conn.close()

    logger.info("========== Anomaly Detection Completed ==========")


if __name__ == "__main__":
    check_price_spikes()