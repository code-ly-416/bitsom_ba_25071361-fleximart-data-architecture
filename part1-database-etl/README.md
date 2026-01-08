# Part 1: Database & ETL Pipeline

## Overview
This section contains the relational database design and ETL pipeline for the Fleximart e-commerce platform. The data flows from raw CSV files through cleaning and transformation into a normalized PostgreSQL database.

## Files in This Directory

- **schema_documentation.md** - Complete database schema with entity descriptions, normalization explanation, and sample data
- **etl_pipeline.py** - Python script that extracts, transforms, and loads data from raw CSVs into PostgreSQL
- **business_queries.sql** - Sample SQL queries for business analysis
- **data_quality_report.txt** - Report showing data cleaning statistics
- **requirements.txt** - Python dependencies

## Quick Start

1. Set up environment variables in `.env`:
   ```
   DB_PASSWORD=your_postgres_password
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the ETL pipeline:
   ```bash
   python etl_pipeline.py
   ```

## Database Schema

Four main tables:
- **customers** - Customer information (contact details, registration date)
- **products** - Product catalog (name, category, price, stock)
- **orders** - Customer orders (order date, status, total amount)
- **order_items** - Line items within orders (quantity, unit price, subtotal)

## Data Transformations

The ETL pipeline handles:
- Duplicate removal
- Date Format Standardization and consistency
- Phone number standardization (E.164 format)
- Missing value fix (filling, defaulting or deletion)
- Surrogate key generation
- Foreign key mapping

## Database Connection

Uses PostgreSQL with SQLAlchemy ORM. Connection configured via environment variables:
- Host: localhost
- Port: 5432
- Database: fleximart
- User: postgres
