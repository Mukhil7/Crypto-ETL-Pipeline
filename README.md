# Crypto ETL Pipeline

## Notice
**This project is private and not intended for public use, modification, or distribution. It is for personal or authorized use only. Unauthorized use, copying, or distribution is strictly prohibited.**

## Overview
Welcome to the Crypto ETL Pipeline! This project demonstrates a scalable ETL (Extract, Transform, Load) workflow for cryptocurrency data using **Apache Airflow**, **PostgreSQL**, **Docker**, and **Python**. It extracts live price data for Bitcoin, Ethereum, Cardano, and Solana from the CoinGecko API, stores it in a PostgreSQL database, and prints the results for verification. The pipeline leverages Airflow's TaskFlow API and dynamic task mapping for efficient processing.

## Features
- **Data Extraction**: Fetches current USD prices for Bitcoin, Ethereum, Cardano, and Solana from the CoinGecko API.
- **Data Storage**: Loads data into a PostgreSQL table (`crypto_prices`) with coin ID, symbol, price, and timestamp.
- **Dynamic Task Mapping**: Uses Airflow's `expand` feature to process each coin individually.
- **Scheduled Execution**: Runs daily with Airflow's scheduling, starting from January 1, 2025.
- **Error Handling**: Includes retry logic (2 retries) and HTTP status checks.
- **Containerized Deployment**: Uses Docker for a reproducible environment.

## Project Contents
- **`dags/crypto_etl_pipeline.py`**: Airflow DAG that orchestrates the ETL process using the TaskFlow API.
- **`scripts/`**: (Optional) Directory for additional ETL scripts (not included in the provided code but can be added).
- **`docker-compose.yml`**: Configuration for spinning up Airflow and PostgreSQL containers.
- **`requirements.txt`**: Lists Python dependencies for the project.
- **`README.md`**: This documentation file.

## Tech Stack
- **Apache Airflow 3**: Orchestrates and schedules ETL tasks.
- **PostgreSQL**: Stores processed cryptocurrency data.
- **Docker**: Provides containerized environments for Airflow and PostgreSQL.
- **Python**: Powers the ETL scripts and Airflow DAGs.
- **CoinGecko API**: Provides live cryptocurrency price data.

## API Used
- **CoinGecko API**: `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,cardano,solana`

## Installation
*Note: Installation is restricted to authorized users only.*

1. Clone the repository (if granted access):
   ```bash
   git clone https://github.com/your-username/crypto-etl-pipeline.git
   cd crypto-etl-pipeline
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `requirements.txt` file with:
   ```
   apache-airflow
   requests
   psycopg2-binary
   ```
4. Set up PostgreSQL and Airflow via Docker:
   - Create or update `docker-compose.yml` based on the sample configuration (see below).
   - Run:
     ```bash
     docker-compose up -d
     ```
5. Initialize the Airflow database:
   ```bash
   airflow db init
   ```
6. Start Airflow services:
   ```bash
   airflow webserver -p 8080
   airflow scheduler
   ```

### Sample `docker-compose.yml`
```yaml
version: '3'
services:
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "5432:5432"
  airflow-webserver:
    image: apache/airflow:latest
    depends_on:
      - postgres
    ports:
      - "8080:8080"
    command: webserver
  airflow-scheduler:
    image: apache/airflow:latest
    depends_on:
      - postgres
    command: scheduler
  airflow-dag-processor:
    image: apache/airflow:latest
    depends_on:
      - postgres
    command: dag-processor
  airflow-triggerer:
    image: apache/airflow:latest
    depends_on:
      - postgres
    command: triggerer
```

## Usage
*Note: Usage is restricted to authorized users only.*

1. Place `crypto_etl_pipeline.py` in the Airflow `dags` folder (e.g., `~/airflow/dags`).
2. Access the Airflow UI at `http://localhost:8080`.
3. Enable the `crypto_pipeline` DAG.
4. Trigger the DAG manually (if needed):
   ```bash
   airflow dags trigger crypto_pipeline
   ```
5. Verify data in PostgreSQL:
   ```sql
   SELECT * FROM crypto_prices;
   ```
6. Check task logs in the Airflow UI for printed coin prices.

### PostgreSQL Connection
- **Host**: `astro_e87a99-postgres-1` (or `localhost` if using Docker)
- **Port**: `5432`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `postgres`

Update the `DB_CONN` dictionary in `crypto_etl_pipeline.py` if your connection details differ.

## Code Structure
- **`dags/crypto_etl_pipeline.py`**:
  - **DAG Definition**: Uses `@dag` decorator with daily scheduling and retry logic.
  - **Tasks**:
    - `fetch_crypto_data`: Fetches price data from CoinGecko API.
    - `save_to_postgres`: Creates and populates the `crypto_prices` table.
    - `print_coin`: Prints coin details using dynamic task mapping.
  - **Database Schema**:
    ```sql
    CREATE TABLE crypto_prices (
        id SERIAL PRIMARY KEY,
        coin_id TEXT,
        symbol TEXT,
        price NUMERIC,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

## How It Works
1. **Extract**: The `fetch_crypto_data` task queries the CoinGecko API for prices of Bitcoin, Ethereum, Cardano, and Solana.
2. **Transform**: Data is formatted into a list of dictionaries with `id`, `symbol`, and `price`.
3. **Load**: The `save_to_postgres` task inserts data into the `crypto_prices` table.
4. **Output**: The `print_coin` task prints each coin's details using Airflow's dynamic task mapping.
5. **Scheduling**: Runs daily at midnight, starting January 1, 2025, with no catch-up.

## Example Output
- **Database Table**:
  ```
  id | coin_id  | symbol | price  | ts
  ---+----------+--------+--------+---------------------
   1 | bitcoin  | btc    | 45000  | 2025-01-01 00:00:00
   2 | ethereum | eth    | 3000   | 2025-01-01 00:00:00
  ```
- **Console Output** (from `print_coin` task):
  ```
  Bitcoin (BTC) is trading at $45000
  Ethereum (ETH) is trading at $3000
  Cardano (ADA) is trading at $1.5
  Solana (SOL) is trading at $150
  ```

## Limitations
- Fixed to four cryptocurrencies (Bitcoin, Ethereum, Cardano, Solana).
- Requires a running PostgreSQL instance and Docker setup.
- CoinGecko API rate limits may apply.
- Minimal data transformation (can be extended).
- No advanced monitoring or alerting.

## Future Improvements
- Add support for additional cryptocurrencies via configuration.
- Implement data transformation (e.g., price trend analysis).
- Add error notifications (e.g., email or Slack).
- Include data validation before loading.
- Support visualization of historical price data.

## License
This project is private and all rights are reserved. Unauthorized use, modification, or distribution is prohibited.

## Contact
This project was built as part of a hands-on Data Engineering learning journey. For questions or authorized collaboration, please contact the project owner.
