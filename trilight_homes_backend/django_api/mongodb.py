# mongodb.py
from pymongo import MongoClient
from django.conf import settings

# Function to get the MongoDB collection
def get_collection(collection_name):
    return settings.mongo_db[collection_name]
