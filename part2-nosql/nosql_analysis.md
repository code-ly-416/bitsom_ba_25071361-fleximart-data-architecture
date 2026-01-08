# NoSQL Analysis for Fleximart Product Catalog

## Section A: Limitations of RDBMS (150 words)

The current relational database has some real issues when dealing with diverse product types. Right now, all products share the same columns - product_name, category, price, and stock_quantity. But what happens when we need to store laptop specifications like RAM, processor, and screen size, while shoes need size, color, and material etc. We will have to either create separate tables for each product type (which means lots of joins) or add more of mostly empty columns to the products table. Both approaches are messy.

When the business wants to add a new product category, we need to run ALTER TABLE commands and potentially deal with downtime. This becomes a very big problem for growth and scalability.

Customer reviews are another hassle. To store them properly, we'd need a separate reviews table with foreign keys. Getting a product with all its reviews requires joins, and the data feels disconnected even though reviews naturally belong to products.

## Section B: NoSQL Benefits (150 words)

MongoDB handles these problems much better because of how it stores data. Each product is a document that can have its own unique fields like a laptop document can include RAM and processor specs, while a shoe document has size and color. They all live in the same collection without forcing unnecessary fields on each other.

Reviews can be embedded directly inside the product document as an array. When you fetch a product, you get all its reviews in one go without any need for joins. This makes querying faster and the data structure more logical since reviews are actually part of the product.

As the catalog grows, MongoDB can scale horizontally by adding more servers and the data gets distributed automatically across machines (in the cloud, or locally), so we can handle millions of products without hitting performance barrier. This is much easier than trying to scale a relational database vertically.

## Section C: Trade-offs (100 words)

MongoDB isn't perfect. First, we lose ACID transactions across multiple documents. In our relational setup, when someone places an order, we can update inventory, create the order, and update customer data all in one safe transaction. With MongoDB, if something fails halfway through, we might end up with inconsistent data unless we write extra code to handle it.

Secondly, MongoDB uses more storage space because it duplicates data. If we embed customer info in orders, that data gets repeated for every order they make. Plus there's no referential integrity, which means that nothing can stop us from adding an order for a customer_id that doesn't exist.
