"""
Builds a single composite dashboard-preview image (KPI cards + core charts)
from the cleaned dataset. This stands in for a Power BI screenshot in
environments where Power BI Desktop isn't available, while using the exact
same underlying metrics as dashboard/dashboard_data_model.md.

Run from the project root:
    python scripts/build_dashboard_preview.py
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

df = pd.read_csv("data/processed/sales_data_clean.csv", parse_dates=["order_date"])

total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
overall_margin = total_profit / total_sales
total_orders = df["order_id"].nunique()
avg_order_value = total_sales / total_orders

fig = plt.figure(figsize=(13, 8))
fig.suptitle("Sales & Revenue Performance Dashboard — Preview", fontsize=16, fontweight="bold", y=0.98)
gs = fig.add_gridspec(3, 4, hspace=0.55, wspace=0.35, top=0.90, bottom=0.07, left=0.06, right=0.97)

kpis = [
    ("Total Sales", f"${total_sales/1e6:,.2f}M"),
    ("Total Profit", f"${total_profit/1e6:,.2f}M"),
    ("Profit Margin", f"{overall_margin:.1%}"),
    ("Avg Order Value", f"${avg_order_value:,.0f}"),
]
for i, (label, value) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                                facecolor="#eef1f7", edgecolor="#c9d2e3", linewidth=1))
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=17, fontweight="bold", color="#2b3a55")
    ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=10, color="#5a6274")

monthly = df.groupby(df["order_date"].dt.to_period("M")).agg(total_sales=("sales", "sum")).sort_index()
ax_trend = fig.add_subplot(gs[1, :])
ax_trend.plot(monthly.index.astype(str), monthly["total_sales"], color="#4C72B0", marker="o", markersize=3)
ax_trend.set_title("Monthly Revenue Trend", fontsize=11, loc="left")
ax_trend.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax_trend.set_xticks(ax_trend.get_xticks()[::3])
ax_trend.tick_params(axis="x", labelrotation=90, labelsize=6)

region = df.groupby("region")["sales"].sum().sort_values(ascending=False)
ax_region = fig.add_subplot(gs[2, 0:2])
region.plot(kind="bar", ax=ax_region, color="#55A868")
ax_region.set_title("Sales by Region", fontsize=11, loc="left")
ax_region.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax_region.tick_params(axis="x", labelrotation=0)
ax_region.set_xlabel("")

category = df.groupby("category")["sales"].sum().sort_values(ascending=False)
ax_cat = fig.add_subplot(gs[2, 2:4])
category.plot(kind="bar", ax=ax_cat, color="#C44E52")
ax_cat.set_title("Sales by Category", fontsize=11, loc="left")
ax_cat.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax_cat.tick_params(axis="x", labelrotation=0)
ax_cat.set_xlabel("")

fig.savefig("images/dashboard_preview.png", dpi=140)
print("Saved images/dashboard_preview.png")
