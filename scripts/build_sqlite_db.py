"""
Loads the cleaned sales dataset into a local SQLite database so the
scripts in sql/ can be run and validated without a separate database
server. This mirrors how the same DDL/queries would run against a
production warehouse (Postgres, SQL Server, Snowflake, etc.).

Run from the project root:
    python scripts/build_sqlite_db.py
"""

import sqlite3

import pandas as pd

CLEAN_CSV_PATH = "data/processed/sales_data_clean.csv"
DB_PATH = "data/processed/sales.db"
SCHEMA_PATH = "sql/01_schema.sql"

if __name__ == "__main__":
    df = pd.read_csv(CLEAN_CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    print(f"Loaded {len(df):,} rows into {DB_PATH} (table: sales)")
