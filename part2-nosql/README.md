# Part 2: NoSQL (MongoDB)

## Overview
This module stores the Fleximart product catalog and reviews in MongoDB to handle flexible schemas and embedded review data.

## Key Files
- `products_catalog.json` – Source product + reviews data to import
- `mongodb_operations.js` – Ready-to-use operations (import, queries, updates, aggregations)
- `nosql_analysis.md` – RDBMS limitations, MongoDB benefits, trade-offs

## Quick Start (Compass)
1) Import data: Compass → `products` collection → `Add Data` → Import `products_catalog.json` (JSON Array).
2) Run queries/aggregations from `mongodb_operations.js` using the Compass Filter or Aggregation tabs.

## Operations Included
- Filter electronics under 50,000 showing name/price/stock
- Avg rating ≥ 4.0 via aggregation on `reviews`
- Add a new review to `ELEC001`
- Average price by category (group + sort)

## Why MongoDB Here
- Flexible documents for varied product attributes (phones, shoes, groceries)
- Embedded reviews retrieved with the product (no joins)
- Easy horizontal scaling when the catalog grows
