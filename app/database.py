# import mongodb client to connect to mongodb
from pymongo import MongoClient
# import os to get environment variables
import os

# Get MongoDB URI and database name from environment variables for better security and flexibility
# If not set, default values are used 
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://admin:Admin12345@cluster1.v3xeerc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
)

# Get the database name from environment variable
DB_NAME = os.getenv("DB_NAME", "inventory_db")

# Connect to MongoDB and get the products collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db["products"]