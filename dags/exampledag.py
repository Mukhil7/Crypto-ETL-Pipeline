from airflow.decorators import dag, task
from pendulum import datetime
import requests
import psycopg2

# Connection details for Postgres
DB_CONN = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "astro_e87a99-postgres-1",
    "port": 5432,
}

@dag(
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "Lenovo", "retries": 2},
    tags=["crypto", "etl", "example"],
)
def crypto_pipeline():
    @task
    def fetch_crypto_data() -> list[dict]:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "ids": "bitcoin,ethereum,cardano,solana"}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        return [{"id": c["id"], "symbol": c["symbol"], "price": c["current_price"]} for c in data]

    @task
    def save_to_postgres(data: list[dict]):
        conn = psycopg2.connect(**DB_CONN)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id SERIAL PRIMARY KEY,
                coin_id TEXT,
                symbol TEXT,
                price NUMERIC,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        for record in data:
            cur.execute(
                "INSERT INTO crypto_prices (coin_id, symbol, price) VALUES (%s, %s, %s)",
                (record["id"], record["symbol"], record["price"]),
            )
        conn.commit()
        cur.close()
        conn.close()
        return "Data saved to Postgres"

    @task
    def print_coin(coin: dict):
        print(f"{coin['id'].title()} ({coin['symbol'].upper()}) is trading at ${coin['price']}")

    coins = fetch_crypto_data()
    save_to_postgres(coins)
    print_coin.expand(coin=coins)

crypto_pipeline()