import sqlite3
import pandas as pd

from logger_config import logger

# Database and report paths
DB_PATH = "database/market_data.db"
REPORT_PATH = "reports/daily_stock_report.xlsx"


def generate_report():
    """
    Generates an Excel report containing the latest stock price
    for each ticker.
    """

    try:
        logger.info("========== Report Generation Started ==========")

        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)

        # Get only the latest record for each stock
        df = pd.read_sql_query(
            """
            SELECT s1.ticker,
                   s1.price,
                   s1.volume,
                   s1.fetched_at
            FROM stock_prices s1
            INNER JOIN
            (
                SELECT
                    ticker,
                    MAX(fetched_at) AS latest_time
                FROM stock_prices
                GROUP BY ticker
            ) s2
            ON s1.ticker = s2.ticker
            AND s1.fetched_at = s2.latest_time
            ORDER BY s1.ticker;
            """,
            conn
        )

        # Export to Excel
        df.to_excel(
            REPORT_PATH,
            index=False,
            sheet_name="Latest Stock Prices"
        )

        conn.close()

        logger.info(f"Excel report generated successfully: {REPORT_PATH}")

    except Exception as e:
        logger.error(f"Error generating report: {e}")


if __name__ == "__main__":
    generate_report()