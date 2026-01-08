# Star Schema Design for Fleximart Data Warehouse

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item

**Business Process:** Sales transactions capturing individual product sales with associated metrics

**Measures (Numeric Facts):**
 - `quantity_sold`: Number of units sold in the transaction
 - `unit_price`: Price per unit at the time of sale (historical pricing)
 - `discount_amount`: Discount applied to the line item (in rupees)
 - `total_amount`: Final amount after discount (quantity_sold × unit_price - discount_amount)

**Foreign Keys:**
 - `date_key` → dim_date (Date when transaction occurred)
 - `product_key` → dim_product (Product being sold)
 - `customer_key` → dim_customer (Customer making the purchase)

---
### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis

**Type:** Conformed dimension

**Attributes (as per schema):**
 - `date_key` (PK): Surrogate key in format YYYYMMDD (e.g., 20240115)
 - `full_date`: Actual calendar date
 - `day_of_week`: Day name (Monday, Tuesday, Wednesday, etc.)
 - `month`: Month number (1-12)
 - `month_name`:January, February, etc.
 - `quarter`: Q1, Q2, Q3, Q4
 - `year`: 2023, 2024, etc.
 - `is_weekend`: Boolean

---

### DIMENSION TABLE: dim_product

**Purpose:** Product information for categorization and drill-down analysis

**Type:** As-is dimension (from source products), aligned to warehouse schema

**Attributes (as per schema):**
 - `product_key` (PK): Surrogate key (integer)
 - `product_id`: Source system identifier
 - `product_name`: Name of the product
 - `category`: Electronics, Fashion, Groceries, etc.
 - `subcategory`: Sub-category for finer grouping.
 - `unit_price`: Price at time of load

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer details for segmentation and geographic analysis

**Type:** As-is dimension aligned to warehouse schema

**Attributes (as per schema):**
 - `customer_key` (PK): Surrogate key (integer)
 - `customer_id`: Source system identifier
 - `customer_name`: Full name of the customer
 - `city`: Customer's city
 - `state`: State (nullable if missing in source)
 - `customer_segment`: Segment classification (nullable; not provided in raw data)

---

## Section 2: Design Decisions

This star schema is built around the "transaction line-item" level, which is simply the most detailed view possible. By saving every single item sold in an order as its own row, we give ourselves the most freedom for future analysis. Because we kept the details, we can group the data however we want later—whether by product, customer, date, or a mix of all three. This level of detail lets us answer specific questions like "How many units of this exact product were sold in January?" or "How much did this specific customer spend on electronics?" without missing any information.

We decided to use "surrogate keys" (simple ID numbers created by our system) instead of using the original IDs from the source data. We do this for a few smart reasons. First, it keeps things stable; if a customer changes their info in the real world, it won't break the links in our database. Second, these keys are just small numbers, which makes the computer much faster when connecting tables compared to using long text IDs. Third, it separates our analysis from the source system, so changes there don't mess up our reports. For dates, we use a simple YYYYMMDD number format so it sorts correctly and is easy to read.

Finally, this design makes it very easy to zoom in and out of the data (drill-down and roll-up). We can easily "roll up" to see monthly totals just by grouping the daily data, or we can "drill down" from a broad category like 'Groceries' to see specific items. Since the main fact table holds the smallest details, and the dimension tables hold the categories, we have everything we need to look at the business from any angle—high level or deep dive.

---

## Section 3: Sample Data Flow

### Source Transaction (from raw sales T005)

```
Order #T005
Customer: Vikram Singh (Customer ID: C005)
Product: Basmati Rice 5kg (Product ID: P009)
Quantity: 3 units
Unit Price: 650.00 rupees
Discount: 0.00 rupees
Total Amount: 3 × 650.00 = 1950.00 rupees
Order Date: 2024-01-20
```

### Data Warehouse Representation (aligned to current schema)

**fact_sales table:**
```
{
  sales_key: 1005,
  date_key: 20240120,
  product_key: 9,
  customer_key: 5,
  quantity_sold: 3,
  unit_price: 650.00,
  discount_amount: 0.00,
  total_amount: 1950.00
}
```

**dim_date table:**
```
{
  date_key: 20240120,
  full_date: 2024-01-20,
  day_of_week: Saturday,
  day_of_month: 20,
  month: 1,
  month_name: January,
  quarter: Q1,
  year: 2024,
  is_weekend: True
}
```

**dim_product table:**
```
{
  product_key: 9,
  product_id: P009,
  product_name: Basmati Rice 5kg,
  category: groceries,
  subcategory: NULL,
  unit_price: 650.00
}
```

**dim_customer table:**
```
{
  customer_key: 5,
  customer_id: C005,
  customer_name: Vikram Singh,
  city: Chennai,
  state: NULL,
  customer_segment: NULL
}
```
