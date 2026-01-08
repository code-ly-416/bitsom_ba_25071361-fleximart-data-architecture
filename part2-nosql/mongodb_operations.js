// MongoDB Compass Operations for Fleximart Product Catalog

// OPERATION 1: Load Data
// In MongoDB Compass: Click "Add Data" button -> Import JSON file -> Select products_catalog.json
// The data will be imported into the 'products' collection automatically


// OPERATION 2: Basic Query
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock

{"category": "Electronics", "price": {"$lt": 50000}}

// OPERATION 3: Review Analysis
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array

[
  {
    "$addFields": {
      "avgRating": {
        "$avg": "$reviews.rating"
      }
    }
  },
  {
    "$match": {
      "avgRating": { "$gte": 4.0 }
    }
  },
  {
    "$project": {
      "name": 1,
      "category": 1,
      "avgRating": 1,
      "reviewCount": { "$size": "$reviews" }
    }
  }
]



// OPERATION 4: Update Operation
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}

{"product_id": "ELEC001"}

{
  "$push": {
    "reviews": {
      "user_id": "U999",
      "username": "NewUser",
      "rating": 4,
      "comment": "Good value",
      "date": new Date()
    }
  }
}





// OPERATION 5: Complex Aggregation
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending

[
  {
    "$group": {
      "_id": "$category",
      "avg_price": { "$avg": "$price" },
      "product_count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "avg_price": -1 }
  },
  {
    "$project": {
      "category": "$_id",
      "avg_price": { "$round": ["$avg_price", 2] },
      "product_count": 1,
      "_id": 0
    }
  }
]



