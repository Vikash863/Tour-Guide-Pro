import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime

load_dotenv()

# MongoDB Connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["tour"]

# Collection references
tours_collection = db["tours"]
users_collection = db["users"]
bookings_collection = db["bookings"]
reviews_collection = db["reviews"]
payments_collection = db["payments"]

# Index creation for better query performance
def create_indexes():
    """Create indexes for production-level performance"""
    try:
        # Tours collection indexes
        tours_collection.create_index("destination")
        tours_collection.create_index("rating")
        tours_collection.create_index([("created_at", -1)])
        
        # Users collection indexes
        users_collection.create_index("email", unique=True)
        users_collection.create_index("phone")
        
        # Bookings collection indexes
        bookings_collection.create_index("user_id")
        bookings_collection.create_index("tour_id")
        bookings_collection.create_index([("created_at", -1)])
        
        # Reviews collection indexes
        reviews_collection.create_index("tour_id")
        reviews_collection.create_index("user_id")
        
        print("MongoDB indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

# MongoDB utility functions
def sanitize_document(doc):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    if doc and isinstance(doc, dict):
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return doc

def sanitize_list(docs):
    """Sanitize list of documents"""
    return [sanitize_document(doc) for doc in docs]

def get_object_id(id_str):
    """Convert string to MongoDB ObjectId"""
    try:
        return ObjectId(id_str)
    except:
        return None

# Initialize indexes on module load
create_indexes()
