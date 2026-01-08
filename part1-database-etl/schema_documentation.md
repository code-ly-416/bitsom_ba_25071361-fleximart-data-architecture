# Fleximart Database Schema Documentation

## 1. Entity-Relationship Description (Text Format)

### ENTITY: customers
**Purpose:** Stores customer information and contact details for order tracking and communication.

**Attributes:**
- `customer_id`: Unique identifier (Primary Key) - SERIAL, auto-incremented surrogate key
- `first_name`: Customer's first name (VARCHAR(50), NOT NULL) - Required field for identification
- `last_name`: Customer's last name (VARCHAR(50), NOT NULL) - Required field for identification
- `email`: Customer's email address (VARCHAR(100)) - Optional field for electronic communication
- `phone`: Customer's phone number (VARCHAR(20)) - Optional field for contact, standardized in E.164 format
- `city`: Customer's city of residence (VARCHAR(50)) - Optional field for delivery and demographic data
- `registration_date`: Date when customer registered (DATE) - Optional field for customer lifecycle tracking

**Relationships:**
- One customer can place MANY orders (1:M with orders table) - A single customer can have multiple orders across time
- Orders table has FOREIGN KEY constraint on `customer_id` referencing `customers(customer_id)`

---

### ENTITY: products
**Purpose:** Maintains product catalog including names, categories, pricing, and inventory levels.

**Attributes:**
- `product_id`: Unique identifier (Primary Key) - SERIAL, auto-incremented surrogate key
- `product_name`: Name of the product (VARCHAR(100), NOT NULL) - Required field for product identification
- `category`: Product category classification (VARCHAR(50)) - Optional field for product grouping and filtering
- `price`: Product unit price (DECIMAL(10,2)) - Optional field for pricing information, supports up to 10 digits with 2 decimal places
- `stock_quantity`: Current inventory quantity (INT, DEFAULT 0) - Required field defaulting to 0 to track available stock

**Relationships:**
- One product can appear in MANY order items (1:M with order_items table) - A single product can be purchased multiple times
- order_items table has FOREIGN KEY constraint on `product_id` referencing `products(product_id)`

---

### ENTITY: orders
**Purpose:** Records customer purchase transactions with order dates, amounts, and fulfillment status.

**Attributes:**
- `order_id`: Unique identifier (Primary Key) - SERIAL, auto-incremented surrogate key
- `customer_id`: Foreign key referencing customers (INT) - Links each order to a customer
- `order_date`: Date when order was placed (DATE) - Required field for transaction tracking and analysis
- `total_amount`: Total amount of order (DECIMAL(10,2)) - Optional field storing aggregated order value
- `status`: Order fulfillment status (VARCHAR(20), DEFAULT 'Pending') - Tracks order lifecycle (Pending, Processing, Shipped, Delivered, etc.)

**Relationships:**
- Many-to-One with customers table - Every order belongs to exactly one customer
- One-to-Many with order_items table - One order can contain multiple line items
- FOREIGN KEY constraint on `customer_id` references `customers(customer_id)`

---

### ENTITY: order_items
**Purpose:** Details the line items within each order, linking products and recording quantities purchased.

**Attributes:**
- `order_item_id`: Unique identifier (Primary Key) - SERIAL, auto-incremented surrogate key
- `order_id`: Foreign key referencing orders (INT, NOT NULL) - Links item to parent order
- `product_id`: Foreign key referencing products (INT, NOT NULL) - Links item to specific product
- `quantity`: Number of units purchased (INT, NOT NULL) - Required field for purchase quantity tracking
- `unit_price`: Price per unit at time of purchase (DECIMAL(10,2)) - Optional field storing historical pricing
- `subtotal`: Total price for this line item (DECIMAL(10,2)) - Optional field storing quantity × unit_price

**Relationships:**
- Many-to-One with orders table - Multiple line items belong to one order
- Many-to-One with products table - Multiple line items can reference one product
- FOREIGN KEY constraint on `order_id` references `orders(order_id)`
- FOREIGN KEY constraint on `product_id` references `products(product_id)`

---

## 2. Normalization Explanation (3NF Design)

### Why This Design is in Third Normal Form (3NF)

This database schema achieves Third Normal Form (3NF) by eliminating redundancies and proper table decomposition. The design satisfies all three normalization requirements:

**First Normal Form (1NF):** All attributes contain atomic values (no multivalued attributes).

**Second Normal Form (2NF):** All non-key attributes are fully functionally dependent on the entire primary key. Since each table uses a single-column surrogate primary key (customer_id, product_id, order_id, order_item_id), this requirement is automatically satisfied. No partial dependencies exist where an attribute depends on only part of a composite key.

**Third Normal Form (3NF):** All non-key attributes depend only on the primary key, eliminating transitive dependencies.

### Functional Dependencies

The key functional dependencies are:
- **Customers:** customer_id → {first_name, last_name, email, phone, city, registration_date}
- **Products:** product_id → {product_name, category, price, stock_quantity}
- **Orders:** order_id → {customer_id, order_date, total_amount, status}
- **Order Items:** order_item_id → {order_id, product_id, quantity, unit_price, subtotal}

### Elimination of Anomalies

**Insert Anomalies:** The decomposed structure prevents forced insertions. New products can be added to the products table independently without creating orders and new customers can be added without requiring orders or order items.

**Delete Anomalies:** Removing an order doesn't delete product information, as they're stored separately.

**Update Anomalies:** Product price changes update only one location in the products table, propagating to future orders while order_items preserves historical unit_price data. Customer information updates in one row affect all associated orders through the foreign key relationship.

---

## 3. Sample Data Representation

### Customers Table
*After ETL transformation with surrogate keys, cleaned phone numbers (E.164 format), and standardized dates*

| customer_id | first_name | last_name | email | phone | city | registration_date |
|---|---|---|---|---|---|---|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | +919876543210 | Bangalore | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | +919988776655 | Mumbai | 2023-02-20 |
| 3 | Amit | Kumar | NULL | +919765432109 | Delhi | 2023-03-10 |

### Products Table
*After ETL transformation with surrogate keys, standardized categories, and filled missing values*

| product_id | product_name | category | price | stock_quantity |
|---|---|---|---|---|
| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |
| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |
| 3 | Apple MacBook Pro | Electronics | 52999.00 | 45 |

### Orders Table
*Derived from sales transactions with aggregated totals and mapped customer/product IDs*

| order_id | customer_id | order_date | total_amount | status |
|---|---|---|---|---|
| 1 | 1 | 2024-01-15 | 45999.00 | Completed |
| 2 | 2 | 2024-01-16 | 5998.00 | Completed |
| 3 | 3 | 2024-01-15 | 52999.00 | Completed |

### Order Items Table
*Line items with historical pricing captured at time of transaction*

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 2 | 4 | 2 | 2999.00 | 5998.00 |
| 3 | 3 | 7 | 1 | 52999.00 | 52999.00 |

---
