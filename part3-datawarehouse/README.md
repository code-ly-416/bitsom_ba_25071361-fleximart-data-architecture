# Part 3: Data Warehouse

## Overview
Star-schema warehouse for Fleximart sales analytics (PostgreSQL). Includes dimensions for date, product, and customer, plus a fact table for sales line items.

## Key Files
- `warehouse_schema.sql` – DDL for dim_date, dim_product, dim_customer, fact_sales
- `warehouse_data.sql` – Sample INSERTs derived from raw CSVs (Jan–Apr 2024)
- `star_schema_design.md` – Schema description, design rationale, sample data flow
- `analytics_queries.sql` – Example analytical queries

## How to Load
1) Create DB and run schema:
```
psql -d fleximart_dw -f warehouse_schema.sql
```
2) Load sample data:
```
psql -d fleximart_dw -f warehouse_data.sql
```

## Table Summary
- `dim_date` – Calendar attributes for time analysis
- `dim_product` – Product catalog (category, price)
- `dim_customer` – Customer info (city/state)
- `fact_sales` – Line-level sales facts (quantity, price, discount, totals)

## Notes
- Data sourced from raw CSVs; missing customer/product mapped to placeholder rows to keep FKs valid.
- Dates cover Jan–Apr 2024; 40 sales rows.
