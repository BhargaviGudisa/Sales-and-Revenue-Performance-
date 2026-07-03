# Dashboard

This folder documents the dashboard layer of the project — the data model,
DAX-style measures, and page layout intended for Power BI Desktop.

> **Note on file contents:** This repository does not include a `.pbix` binary
> (Power BI Desktop is not part of this environment's build pipeline, and
> `.pbix` files are opaque binaries that don't diff well in Git). Instead,
> this folder documents the exact dashboard design and measures, and a
> generated preview image (`images/dashboard_preview.png`) shows the KPIs and
> visuals rendered from the same underlying dataset. Anyone with Power BI
> Desktop can rebuild the file in minutes using `data/processed/sales_data_clean.csv`
> and the measures below.

## Data source

Single table load from `data/processed/sales_data_clean.csv` (or the SQLite
database produced by `scripts/build_sqlite_db.py`), imported as the `sales`
table.

## Suggested measures (DAX)

```
Total Sales        = SUM(sales[sales])
Total Profit       = SUM(sales[profit])
Profit Margin      = DIVIDE([Total Profit], [Total Sales])
Total Orders       = DISTINCTCOUNT(sales[order_id])
Avg Order Value    = DIVIDE([Total Sales], [Total Orders])
Total Customers    = DISTINCTCOUNT(sales[customer_id])
MoM Sales Growth   = DIVIDE([Total Sales] - CALCULATE([Total Sales], DATEADD(sales[order_date], -1, MONTH)),
                            CALCULATE([Total Sales], DATEADD(sales[order_date], -1, MONTH)))
```

## Page layout

**Page 1 — Executive Overview**
- KPI cards: Total Sales, Total Profit, Profit Margin, Avg Order Value
- Line chart: monthly revenue trend
- Bar chart: sales by region
- Bar chart: sales by category
- Slicers: order date range, region, category, segment

**Page 2 — Product & Category Analysis**
- Bar chart: top 10 products by revenue
- Table: sub-category revenue / profit / margin
- Scatter or bar: high-volume, low-margin products flagged for review

**Page 3 — Customer & Regional Analysis**
- Table: top 10 customers by lifetime revenue
- Map or bar chart: region x category cross-tab
- Segment breakdown (Consumer / Corporate / Home Office)

## Preview

See [`images/dashboard_preview.png`](../images/dashboard_preview.png) for a
KPI + chart preview generated directly from the cleaned dataset via
`scripts/build_dashboard_preview.py`.
