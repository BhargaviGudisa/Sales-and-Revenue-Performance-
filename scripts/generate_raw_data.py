"""
Generates a synthetic retail sales transactions dataset for the
Sales and Revenue Performance Dashboard portfolio project.

The output intentionally contains realistic data-quality issues
(nulls, duplicates, inconsistent casing, mixed date formats) so the
cleaning step in scripts/clean_data.py has real work to demonstrate.

Run from the project root:
    python scripts/generate_raw_data.py
"""

import random
from datetime import timedelta

import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ROWS = 9800
OUTPUT_PATH = "data/raw/sales_data_raw.csv"

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

REGIONS = {
    "East": ["New York", "Boston", "Philadelphia", "Newark"],
    "West": ["Los Angeles", "San Francisco", "Seattle", "San Diego"],
    "Central": ["Chicago", "Dallas", "Houston", "Detroit"],
    "South": ["Atlanta", "Miami", "Orlando", "Charlotte"],
}
STATE_BY_CITY = {
    "New York": "New York", "Boston": "Massachusetts", "Philadelphia": "Pennsylvania", "Newark": "New Jersey",
    "Los Angeles": "California", "San Francisco": "California", "Seattle": "Washington", "San Diego": "California",
    "Chicago": "Illinois", "Dallas": "Texas", "Houston": "Texas", "Detroit": "Michigan",
    "Atlanta": "Georgia", "Miami": "Florida", "Orlando": "Florida", "Charlotte": "North Carolina",
}

CATEGORY_TREE = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

FIRST_NAMES = ["James", "Maria", "Robert", "Linda", "Michael", "Patricia", "David", "Jennifer",
               "William", "Elizabeth", "Carlos", "Sofia", "Ahmed", "Wei", "Priya", "Fatima"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Garcia", "Miller", "Davis", "Martinez",
              "Lopez", "Wilson", "Anderson", "Thomas", "Chen", "Khan", "Patel", "Kim"]

PRODUCT_NAME_POOL = {
    "Chairs": ["Executive Leather Chair", "Mesh Task Chair", "Stackable Conference Chair", "Ergonomic Office Chair"],
    "Tables": ["Round Conference Table", "Adjustable Height Desk", "Glass Top Coffee Table", "Folding Utility Table"],
    "Bookcases": ["5-Shelf Bookcase", "Corner Bookcase", "Modular Bookcase Unit"],
    "Furnishings": ["Desk Lamp", "Task Chair Cushion", "Wall Clock", "Filing Cabinet"],
    "Binders": ["3-Ring Binder", "View Binder", "Heavy-Duty Binder"],
    "Paper": ["Multipurpose Copy Paper", "Recycled Printer Paper", "Cardstock Paper"],
    "Storage": ["Storage Box, Letter Size", "Plastic Storage Bin", "Metal Storage Cabinet"],
    "Art": ["Round Pencils", "Highlighter Set", "Sketch Pad"],
    "Labels": ["Round Labels", "Shipping Labels", "Address Labels"],
    "Phones": ["Smartphone X200", "Cordless Phone", "VoIP Desk Phone"],
    "Machines": ["Laser Printer", "Label Maker", "Fax Machine"],
    "Accessories": ["Wireless Mouse", "USB Keyboard", "Laptop Stand"],
    "Copiers": ["Desktop Copier", "Office Copier Pro"],
}

UNIT_COST_RANGE = {
    "Furniture": (60, 900), "Office Supplies": (2, 120), "Technology": (30, 1800)
}
MARGIN_RANGE = {
    "Furniture": (-0.15, 0.25), "Office Supplies": (0.05, 0.40), "Technology": (-0.05, 0.30)
}

start_date = pd.Timestamp("2021-01-01")
end_date = pd.Timestamp("2023-12-31")
date_range_days = (end_date - start_date).days


def random_order_date():
    return start_date + timedelta(days=random.randint(0, date_range_days))


def format_date_messy(d: pd.Timestamp) -> str:
    """Return the date in one of several formats to mimic real-world messy exports."""
    fmt = random.choice(["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%m/%d/%y"])
    return d.strftime(fmt)


rows = []
for i in range(N_ROWS):
    order_id = f"ORD-{2021 + (i % 3)}-{100000 + i}"
    order_date = random_order_date()
    ship_days = random.choice([1, 2, 3, 4, 5, 7])
    ship_date = order_date + timedelta(days=ship_days)

    customer_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    customer_id = f"CUST-{abs(hash(customer_name)) % 5000:05d}"
    segment = random.choice(SEGMENTS)

    region = random.choice(list(REGIONS.keys()))
    city = random.choice(REGIONS[region])
    state = STATE_BY_CITY[city]

    category = random.choices(list(CATEGORY_TREE.keys()), weights=[0.25, 0.45, 0.30])[0]
    sub_category = random.choice(CATEGORY_TREE[category])
    product_name = random.choice(PRODUCT_NAME_POOL[sub_category])
    product_id = f"{category[:3].upper()}-{sub_category[:3].upper()}-{abs(hash(product_name)) % 9999:04d}"

    quantity = random.randint(1, 12)
    unit_cost = round(random.uniform(*UNIT_COST_RANGE[category]), 2)
    discount = random.choices([0, 0.1, 0.15, 0.2, 0.3, 0.5], weights=[0.35, 0.2, 0.15, 0.15, 0.1, 0.05])[0]
    margin = random.uniform(*MARGIN_RANGE[category])

    gross_sales = round(unit_cost * quantity, 2)
    sales = round(gross_sales * (1 - discount), 2)
    profit = round(sales * margin, 2)

    ship_mode = random.choice(SHIP_MODES)

    # Introduce messiness for the cleaning step to fix:
    category_display = category.upper() if random.random() < 0.08 else category
    region_display = region.lower() if random.random() < 0.05 else region
    postal_code = "" if random.random() < 0.04 else str(random.randint(10000, 99999))
    order_date_str = format_date_messy(order_date)
    ship_date_str = format_date_messy(ship_date)

    rows.append({
        "Order ID": order_id,
        "Order Date": order_date_str,
        "Ship Date": ship_date_str,
        "Ship Mode": ship_mode,
        "Customer ID": customer_id,
        "Customer Name": customer_name,
        "Segment": segment,
        "Region": region_display,
        "City": city,
        "State": state,
        "Postal Code": postal_code,
        "Category": category_display,
        "Sub-Category": sub_category,
        "Product ID": product_id,
        "Product Name": product_name,
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# Duplicate ~1.5% of rows to mimic export duplication errors
dup_frac = 0.015
dup_rows = df.sample(frac=dup_frac, random_state=RANDOM_SEED)
df = pd.concat([df, dup_rows], ignore_index=True)

# Null out a few Customer Name / Profit values to mimic missing data
null_idx = df.sample(frac=0.01, random_state=RANDOM_SEED + 1).index
df.loc[null_idx, "Profit"] = np.nan

df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)  # shuffle

df.to_csv(OUTPUT_PATH, index=False)
print(f"Wrote {len(df):,} rows to {OUTPUT_PATH}")
