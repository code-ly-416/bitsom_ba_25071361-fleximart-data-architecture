# FlexiMart Data Architecture Project

**Student Name:** Lavya Jaitly
**Student ID:** bitsom_ba_25071361
**Email:** jaitlylavya@gmail.com
**Date:** 2026-01-08

## Project Overview

End-to-end data pipeline for FlexiMart: cleaned CSV source data, loaded it into PostgreSQL, analyzed with SQL, modeled a MongoDB product catalog for flexible attributes, and built a star-schema warehouse for historical sales analytics.

## Repository Structure

```
fleximart-data-architecture/
├── data/
│   ├── customers_raw.csv
│   ├── products_raw.csv
│   └── sales_raw.csv
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   ├── data_quality_report.txt
│   ├── README.md
│   └── requirements.txt
├── part2-nosql/
│   ├── mongodb_operations.js
│   ├── nosql_analysis.md
│   ├── products_catalog.json
│   └── README.md
├── part3-datawarehouse/
│   ├── analytics_queries.sql
│   ├── star_schema_design.md
│   ├── warehouse_data.sql
│   ├── warehouse_schema.sql
│   └── README.md
└── README.md
```

## Technologies Used

- Python 3, pandas, SQLAlchemy
- PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Set DB password in .env
create .env file in root directory
echo DB_PASSWORD=your_postgres_password > .env

# Create databases
createdb fleximart
createdb fleximart_dw

# Run Part 1 - ETL Pipeline (loads raw CSVs into PostgreSQL fleximart)
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
psql -d fleximart -f part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
psql -d fleximart_dw -f part3-datawarehouse/warehouse_schema.sql
psql -d fleximart_dw -f part3-datawarehouse/warehouse_data.sql
psql -d fleximart_dw -f part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js
or via mongodb compass

## Key Learnings

- I got comfortable cleaning messy CSVs with pandas (dates, phones, prices) and seeing how much cleaner the data can become after a solid pipeline.
- I also learned how to wire that cleaned data into PostgreSQL and how a clear schema plus good keys make queries simpler.
- Overall, I saw how the pieces fit from raw data to analytics.

## Challenges Faced

1. First time using pgAdmin—took a bit to navigate and get comfortable running scripts there.
2. First time taking raw data from zero to a complete project—figuring out the flow.
