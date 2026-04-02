# Import FastAPI tools
from fastapi import FastAPI, HTTPException

# Import the MongoDB collection
from app.database import products_collection

# Import the Product schema for validation
from app.schemas import Product

# Import requests so we can call the currency exchange API
import requests

# Create the FastAPI app
app = FastAPI(title="Inventory Management API")


# Home route to check if the API is running
@app.get("/")
def home():
    return {"message": "Inventory API is running"}


# Get all products from the database
@app.get("/getAll")
def get_all():
    # Get every product and remove MongoDB's _id field
    products = list(products_collection.find({}, {"_id": 0}))
    return products


# Get one product by ProductID
@app.get("/getSingleProduct")
def get_single_product(product_id: int):
    # Search for one product with the matching ProductID
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})

    # If nothing is found, return an error
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# Add a new product to the database
@app.post("/addNew")
def add_new(product: Product):
    # Check if the ProductID already exists
    existing_product = products_collection.find_one({"ProductID": product.ProductID})

    # If it exists, do not insert it again
    if existing_product:
        raise HTTPException(status_code=400, detail="ProductID already exists")

    # Insert the new product into MongoDB
    products_collection.insert_one(product.dict())

    return {"message": "Product added successfully"}


# Delete one product by ProductID
@app.delete("/deleteOne")
def delete_one(product_id: int):
    # Delete the product with the matching ProductID
    result = products_collection.delete_one({"ProductID": product_id})

    # If no product was deleted, it was not found
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


# Get all products whose name starts with a given letter
@app.get("/startsWith")
def starts_with(letter: str):
    # Make sure only one character is entered
    if len(letter) != 1:
        raise HTTPException(status_code=400, detail="Please enter one letter only")

    # MongoDB regex to find names starting with the given letter
    products = list(
        products_collection.find(
            {"Name": {"$regex": f"^{letter}", "$options": "i"}},
            {"_id": 0}
        )
    )

    return products


# Get up to 10 products between two ProductIDs
@app.get("/paginate")
def paginate(start_id: int, end_id: int):
    # Find products in the ProductID range, sort them, and limit to 10
    products = list(
        products_collection.find(
            {"ProductID": {"$gte": start_id, "$lte": end_id}},
            {"_id": 0}
        ).sort("ProductID", 1).limit(10)
    )

    return products


# Convert a product's USD price into EUR
@app.get("/convert")
def convert(product_id: int):
    # Find the product first
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})

    # If not found, return an error
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Call an online exchange-rate API
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    # If the API fails, return an error
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Exchange rate API failed")

    # Read the JSON response
    data = response.json()

    # Get the EUR rate
    eur_rate = data["rates"]["EUR"]

    # Convert the product price to EUR
    eur_price = round(product["UnitPrice"] * eur_rate, 2)

    # Return the conversion result
    return {
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "PriceUSD": product["UnitPrice"],
        "PriceEUR": eur_price,
        "ExchangeRate": eur_rate
    }