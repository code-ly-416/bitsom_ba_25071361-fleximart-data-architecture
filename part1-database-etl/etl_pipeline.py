
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import phonenumbers

# Loading the environment variables from .env file
load_dotenv('../.env', override=True)

# 1. Configuring db connection. (with env)

db_password = os.getenv('DB_PASSWORD')  # Reads from .env
db_user = 'postgres'
db_host = 'localhost'
db_port = '5432'
db_name = 'fleximart'

# logging to verify the connection
if not db_password:
    print("Error: DB_PASSWORD not found. Check your .env file.")
else:
    # Connecting to Postgres Database
    try:
        connection_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(connection_str)
        with engine.connect() as conn:
            print("Connected to Database using secure password.")
    except Exception as e:
        print(f"Connection Failed: {e}")


# Schema Creation Commands
schema_commands = """
-- 1. DROP TABLES (Order matters due to dependencies)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- 2. CREATE CUSTOMERS
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date DATE
);

-- 3. CREATE PRODUCTS
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0
);

-- 4. CREATE ORDERS
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 5. CREATE ORDER ITEMS
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

# Execution
with engine.connect() as conn:
    conn.execute(text(schema_commands))
    conn.commit()

print("Schema created successfully (All tables reset).")


# Extraction function and calling it
def extract_data():
    # Reads csv files and returns dataframes
    try:
        # Read csv files
        c_df = pd.read_csv('../data/customers_raw.csv')
        p_df = pd.read_csv('../data/products_raw.csv')
        s_df = pd.read_csv('../data/sales_raw.csv')

        print("Data Extracted Successfully")
        return c_df, p_df, s_df

    except FileNotFoundError as e:
        print(f"Extraction Failed: {e}")
        return None, None, None

# Calling the function
raw_customers, raw_products, raw_sales = extract_data()


# Cleaning Customers Data
print("Cleaning Customers Data...")
# Removing duplicates
raw_customers = raw_customers.drop_duplicates(subset=['customer_id'], keep='first')
print(f"Filtered. Rows remaining: {len(raw_customers)}")


# phone number cleaning
def clean_phone_number(phone_str):
    try:
        # Parse the number. "IN" is the default region if +91 is missing.
        parsed_num = phonenumbers.parse(str(phone_str), "IN")

        # Check if valid
        if phonenumbers.is_valid_number(parsed_num):
            # Format to standard E.164 (e.g., +919876543210)
            return phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None # Invalid number becomes NaN
    except phonenumbers.NumberParseException:
        return None

raw_customers['phone'] = raw_customers['phone'].apply(clean_phone_number)
print("Phone Numbers Standardized.")


# Convert date to YYYY-MM-DD
raw_customers['registration_date'] = pd.to_datetime(
    raw_customers['registration_date'],
    dayfirst=True,
    format='mixed',
    errors='coerce'
).dt.date
print("Registration Dates Standardized.")


# Capitalize first letter of each word
raw_customers['city'] = raw_customers['city'].str.title()
print("City Names Standardized.")


# Preserve Old IDs by renaming the column
raw_customers.rename(columns={'customer_id': 'source_id'}, inplace=True)

# Adding Surrogate Key
raw_customers.insert(0, 'customer_id', range(1, 1 + len(raw_customers)))


# 1. Fill empty cells with the text "NULL" to keep things simple
df_ready = raw_customers.fillna("NULL")


print("Loading Customers...")
cols_customers = ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'city', 'registration_date']
raw_customers[cols_customers].to_sql('customers', engine, if_exists='append', index=False)


# Cleaning Products Data
print("Cleaning Products Data...")
# Removing duplicates
raw_products = raw_products.drop_duplicates()
print(f"Filtered. Rows remaining: {len(raw_products)}")


# Standardizing Category Names
raw_products['category'] = raw_products['category'].str.title()
print("Category Names Standardized.")


# Cleaning Product Names
raw_products['product_name'] = raw_products['product_name'].str.strip()
print("Product Names Cleaned.")


# Handle Missing values
print("Handling Missing Values...")
# Filling missing price from sales data
# Get Price from Sales
price_map = raw_sales.dropna(subset=['unit_price']).drop_duplicates('product_id').set_index('product_id')['unit_price']

# Fill missing 'price' in products using the Sales map
raw_products['price'] = raw_products['price'].fillna(raw_products['product_id'].map(price_map))

# Filling if still missing
raw_products['price'] = raw_products.groupby('category')['price'].transform(lambda x: x.fillna(x.mean()))
# Stock: DEFAULT to 0
raw_products['stock_quantity'] = raw_products['stock_quantity'].fillna(0).astype(int)


# Surrogate Keys
# Renaming old ID to 'source_id'
raw_products.rename(columns={'product_id': 'source_id'}, inplace=True)
# Add surrogate key
raw_products.insert(0, 'product_id', range(1, 1 + len(raw_products)))


print("Products Transformed.")

# Loading Products
print("Loading Products...")
cols_products = ['product_id', 'product_name', 'category', 'price', 'stock_quantity']
raw_products[cols_products].to_sql('products', engine, if_exists='append', index=False)

print("Cleaning Orders Data...")
# Removing duplicates
raw_sales = raw_sales.drop_duplicates()
print(f"Order Duplicates Removed. Rows remaining: {len(raw_sales)}")


# Standardize Date
print("Standardizing Dates...")
raw_sales['transaction_date'] = pd.to_datetime(
    raw_sales['transaction_date'],
    dayfirst=True,
    format='mixed',
    errors='coerce'
).dt.date


# Calculate Total Amount
raw_sales['total_amount'] = raw_sales['quantity'] * raw_sales['unit_price']

print("Dates cleaned and Totals calculated.")


# 1. Create a simple lookup dictionary: coo1 : 1 coo2 : 2...
customer_map = dict(zip(raw_customers['source_id'], raw_customers['customer_id']))
product_map = dict(zip(raw_products['source_id'], raw_products['product_id']))

# 2. Direct Overwrite
raw_sales['customer_id'] = raw_sales['customer_id'].map(customer_map)
raw_sales['product_id'] = raw_sales['product_id'].map(product_map)

print("IDs Overwritten in raw_sales.")

# Surrogate Keys
# Renaming old ID to 'source_id'
raw_sales.rename(columns={'transaction_id': 'source_id'}, inplace=True)
# Add surrogate key
raw_sales.insert(0, 'order_id', range(1, 1 + len(raw_sales)))


raw_sales.rename(columns={'transaction_date': 'order_date'}, inplace=True)
# Loading Orders
print("Loading Orders...")
cols_order = ['order_id', 'customer_id', 'order_date', 'total_amount', 'status']
raw_sales[cols_order].to_sql('orders', engine, if_exists='append', index=False)


# Clean & Sort for Order Items
print("Cleaning & Sorting for Order Items...")
raw_sales.dropna(subset=['product_id'], inplace=True)
raw_sales.sort_values('order_date', inplace=True)

# Add Surrogate key
raw_sales.insert(0, 'order_item_id', range(1, 1 + len(raw_sales)))


raw_sales.rename(columns={'total_amount': 'subtotal'}, inplace=True)
# Loading Order Items
print("Loading Order Items...")
cols_order_item = ['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal']
raw_sales[cols_order_item].to_sql('order_items', engine, if_exists='append', index=False)

# Reload original raw files temporarily just to calculate initial stats
orig_cust = pd.read_csv('../data/customers_raw.csv')
orig_prod = pd.read_csv('../data/products_raw.csv')
orig_sales = pd.read_csv('../data/sales_raw.csv')

# Calculate Stats
report = f"""
================================
DATA QUALITY REPORT
Generated: {pd.Timestamp.now()}
================================

1. CUSTOMERS FILE
   - Records Processed:       {len(orig_cust)}
   - Duplicates (in raw):     {len(orig_cust) - len(orig_cust.drop_duplicates())}
   - Missing Values Handled:  {orig_cust.isna().sum().sum()}
   - Records Loaded to DB:    {len(raw_customers)}

2. PRODUCTS FILE
   - Records Processed:       {len(orig_prod)}
   - Duplicates (in raw):     {len(orig_prod) - len(orig_prod.drop_duplicates())}
   - Missing Values Handled:  {orig_prod.isna().sum().sum()}
   - Records Loaded to DB:    {len(raw_products)}

3. SALES FILE (Orders & Items)
   - Records Processed:       {len(orig_sales)}
   - Duplicates (in raw):     {len(orig_sales) - len(orig_sales.drop_duplicates())}
   - Missing Values Handled:  {orig_sales.isna().sum().sum()}
   - Unique Orders Loaded:    {len(raw_sales['order_id'].unique())}
   - Line Items Loaded:       {len(raw_sales['order_item_id'].unique())}

"""

# Append to file if exists, Create if not ('a' mode handles both)
with open('data_quality_report.txt', 'a') as f:
    f.write(report)

print("Report Appended: data_quality_report.txt")
