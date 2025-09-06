Overview

========

Welcome to the Crypto ETL Pipeline! This project demonstrates building a scalable ETL workflow for cryptocurrency data using Apache Airflow, Docker, PostgreSQL, and Linux. The project extracts live cryptocurrency data from the CoinGecko API, transforms it, and loads it into a PostgreSQL database. It also showcases dynamic task mapping for workflow orchestration.

Project Contents

================

Your project contains the following files and folders:

dags: Contains the Python files for your Airflow DAGs. For example:

crypto_etl_pipeline.py: A DAG that extracts cryptocurrency data from the CoinGecko API, transforms it, and loads it into Postgres. The DAG uses the TaskFlow API and dynamic task mapping to handle multiple coins efficiently.

scripts: Python scripts for ETL tasks like data extraction, transformation, and loading.

docker-compose.yml: Configuration to spin up Docker containers for Airflow services and Postgres.

requirements.txt: Python dependencies for Airflow DAGs and ETL scripts.

README.md: Project documentation (this file).

Deploy Your Project Locally

===========================

Start Airflow and your ETL pipeline locally by running:

docker-compose up -d


This command will spin up the following Docker containers:

Postgres: The relational database for storing processed cryptocurrency data

Scheduler: Monitors and triggers Airflow tasks

DAG Processor: Parses your DAG files

API Server: Serves the Airflow UI at http://localhost:8080

Triggerer: Triggers deferred tasks in Airflow

You can also access your Postgres database at localhost:5432 with:

Username: postgres

Password: postgres

Running the DAG

================

Trigger the DAG using the Airflow CLI or UI:

airflow dags trigger crypto_etl_pipeline


The DAG will:

Extract cryptocurrency data from the CoinGecko API

Transform and clean the data

Load it into Postgres

Dynamically map tasks for each coin

Tech Stack

================

Apache Airflow 3 – Orchestration and scheduling of ETL tasks

PostgreSQL – Relational database for structured storage

Docker – Containerization for reproducible environments

Ubuntu Linux – Operating system for managing containers and deployment

Python – Core language for ETL scripts and Airflow DAGs

API Used

================

CoinGecko API: https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,cardano,solana

Contact

================

This project was built as part of a hands-on Data Engineering learning journey.
For questions, suggestions, or collaboration, feel free to reach out!