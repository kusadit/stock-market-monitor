# Stock Market Monitoring Pipeline

## Overview

The Stock Market Monitoring Pipeline is an automated data engineering project that fetches live stock market data from Yahoo Finance, stores it in a SQLite database, detects anomalies in stock prices, generates Excel reports, and automates execution using GitHub Actions.

The project demonstrates the complete lifecycle of a data pipeline, including data collection, storage, monitoring, reporting, logging, and workflow automation.

---

## Features

- Fetches live stock market data using the Yahoo Finance API
- Stores stock prices and trading volume in a SQLite database
- Detects abnormal price movements based on configurable thresholds
- Logs API failures and missing data
- Generates Excel reports containing the latest stock prices
- Uses structured logging for monitoring and debugging
- Automates execution through GitHub Actions
- Designed with a modular and maintainable project structure

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Database | SQLite |
| Data Source | Yahoo Finance (yfinance) |
| Data Analysis | Pandas |
| Reporting | OpenPyXL |
| Automation | GitHub Actions |
| Version Control | Git & GitHub |

---

## Project Structure

```
stock-market-monitor/
│
├── .github/
│   └── workflows/
│       └── run_pipeline.yml
│
├── database/
│   ├── database.py
│   └── market_data.db
│
├── logs/
│   └── application.log
│
├── reports/
│   └── daily_stock_report.xlsx
│
├── fetch_data.py
├── check_anomalies.py
├── report_generator.py
├── logger_config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Workflow

```
GitHub Actions
        │
        ▼
Fetch Live Stock Data
        │
        ▼
Store Data in SQLite
        │
        ▼
Detect Price Anomalies
        │
        ▼
Generate Excel Report
        │
        ▼
Upload Report as GitHub Artifact
```

---

## Database Schema

### stock_prices

| Column | Description |
|---------|-------------|
| id | Primary Key |
| ticker | Stock Symbol |
| price | Closing Price |
| volume | Trading Volume |
| fetched_at | Timestamp |

### alerts

| Column | Description |
|---------|-------------|
| id | Primary Key |
| ticker | Stock Symbol |
| alert_type | API_FAILURE, MISSING_DATA, PRICE_SPIKE |
| message | Alert Description |
| created_at | Timestamp |

---

## Installation

Clone the repository.

```bash
git clone https://github.com/kusadit/stock-market-monitor.git

cd stock-market-monitor
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Usage

Fetch live stock data.

```bash
python fetch_data.py
```

Check for anomalies.

```bash
python check_anomalies.py
```

Generate the Excel report.

```bash
python report_generator.py
```

---

## GitHub Actions

The project includes a GitHub Actions workflow that automates the pipeline.

Workflow steps:

1. Checkout repository
2. Install Python
3. Install project dependencies
4. Fetch stock market data
5. Detect anomalies
6. Generate Excel report
7. Upload report as a workflow artifact

The workflow can be triggered manually from the GitHub Actions tab.

---

## Logging

The application uses Python's built-in logging module.

Logs include:

- Data fetching
- Successful database inserts
- Missing market data
- API failures
- Price spike detection
- Report generation

Logs are stored in:

```
logs/application.log
```

---

## Sample Report

The generated Excel report contains the most recent record for each monitored stock.

| Ticker | Price | Volume | Last Updated |
|---------|-------|---------|--------------|
| RELIANCE.NS | 1327.20 | 18,302,218 | 2026-07-19 |
| TCS.NS | 2269.00 | 5,615,138 | 2026-07-19 |
| INFY.NS | 1096.50 | 12,547,728 | 2026-07-19 |
| HDFCBANK.NS | 819.60 | 17,415,322 | 2026-07-19 |

---

## Future Improvements

- Interactive Streamlit dashboard
- Email notifications for alerts
- Slack integration
- Docker support
- PostgreSQL/MySQL support
- Historical trend visualization
- Unit and integration testing
- REST API for querying stock data

---

## Skills Demonstrated

- Python Programming
- SQL
- SQLite
- Data Engineering
- ETL Pipeline Development
- REST API Integration
- Pandas
- Excel Report Generation
- Logging
- Exception Handling
- Git
- GitHub
- GitHub Actions
- Workflow Automation

---

## License

This project is intended for educational and portfolio purposes.
