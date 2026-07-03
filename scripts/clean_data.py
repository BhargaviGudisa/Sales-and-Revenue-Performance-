"""
Cleans and prepares the raw sales export for analysis and dashboarding.

Steps performed:
    1. Standardize column names (snake_case)
    2. Parse mixed-format date strings into a single datetime format
    3. Normalize inconsistent text casing (Category, Region)
    4. Remove exact duplicate transactions
    5. Handle missing values (Profit, Postal Code)
    6. Add derived fields used throughout the SQL/notebook analysis
       (profit_margin, order_year, order_month, order_year_month)

Run from the project root:
    python scripts/clean_data.py
"""

import pandas as pd

RAW_PATH = "data/raw/sales_data_raw.csv"
PROCESSED_PATH = "data/processed/sales_data_clean.csv"


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def parse_mixed_dates(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="mixed", dayfirst=False, errors="coerce")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)

    df["order_date"] = parse_mixed_dates(df["order_date"])
    df["ship_date"] = parse_mixed_dates(df["ship_date"])

    df["category"] = df["category"].str.strip().str.title()
    df["region"] = df["region"].str.strip().str.title()
    df["sub_category"] = df["sub_category"].str.strip()
    df["customer_name"] = df["customer_name"].str.strip()

    before = len(df)
    df = df.drop_duplicates().copy()
    removed_dupes = before - len(df)

    df["postal_code"] = df["postal_code"].astype("string").replace("", pd.NA)

    missing_profit = df["profit"].isna().sum()
    df["profit"] = df["profit"].fillna(df.groupby("sub_category")["profit"].transform("median"))

    df["profit_margin"] = (df["profit"] / df["sales"]).round(4)
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)

    df = df.dropna(subset=["order_date", "sales"])

    print(f"Removed {removed_dupes} duplicate rows")
    print(f"Imputed {missing_profit} missing profit values using sub-category median")
    print(f"Final row count: {len(df):,}")

    return df


if __name__ == "__main__":
    raw_df = pd.read_csv(RAW_PATH)
    clean_df = clean(raw_df)
    clean_df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved cleaned dataset to {PROCESSED_PATH}")
