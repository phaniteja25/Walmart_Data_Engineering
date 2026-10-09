import os
import sys

import psycopg2

DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "walmart_dataset", "data"
)

# Load order chosen so parent-ish tables load before dependent ones.
TABLES = [
    "customers",
    "stores",
    "products",
    "employees",
    "orders",
    "order_items",
]

COPY_SQL = """
    COPY raw.{table} FROM STDIN WITH (
        FORMAT csv,
        HEADER true,
        DELIMITER ',',
        QUOTE '"'
    )
"""


def main():
    conn_str = os.environ["WALMART_DB_URL"]
    conn = psycopg2.connect(conn_str)
    try:
        with conn:
            with conn.cursor() as cur:
                for table in TABLES:
                    csv_path = os.path.join(DATA_DIR, f"{table}.csv")
                    with open(csv_path, "r", newline="") as f:
                        cur.copy_expert(COPY_SQL.format(table=table), f)
                    cur.execute(f"SELECT COUNT(*) FROM raw.{table}")
                    count = cur.fetchone()[0]
                    print(f"Loaded {table}: {count} rows")
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
