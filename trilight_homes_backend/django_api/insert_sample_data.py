from pymongo import MongoClient
from bson import ObjectId
import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string if different
db = client['trilight_homes-db']  # Update with your database name

# Sample data for properties
properties = [
    {
        "_id": ObjectId(),
        "title": "Luxury Beachfront Villa",
        "description": "A stunning 5-bedroom villa with direct beach access",
        "price": 1500000,
        "bedrooms": 5,
        "bathrooms": 4,
        "area": 350,  # in square meters
        "location": {
            "address": "123 Coastal Road",
            "city": "Malibu",
            "state": "California",
            "country": "USA",
            "zip_code": "90265"
        },
        "amenities": ["pool", "beach access", "gym", "home theater"],
        "status": "for sale",
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    },
    {
        "_id": ObjectId(),
        "title": "Modern Downtown Apartment",
        "description": "A chic 2-bedroom apartment in the heart of the city",
        "price": 500000,
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 100,  # in square meters
        "location": {
            "address": "456 Urban Street",
            "city": "New York",
            "state": "New York",
            "country": "USA",
            "zip_code": "10001"
        },
        "amenities": ["doorman", "fitness center", "rooftop terrace"],
        "status": "for sale",
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }
]

# Sample data for property attributes
attributes = [
    {
        "_id": ObjectId(),
        "name": "Year Built",
        "type": "number"
    },
    {
        "_id": ObjectId(),
        "name": "Parking Spaces",
        "type": "number"
    },
    {
        "_id": ObjectId(),
        "name": "Heating Type",
        "type": "string"
    }
]

# Sample data for property images
images = [
    {
        "_id": ObjectId(),
        "property_id": properties[0]["_id"],
        "url": "https://example.com/image1.jpg",
        "caption": "Beachfront view",
        "is_primary": True,
        "created_at": datetime.datetime.utcnow()
    },
    {
        "_id": ObjectId(),
        "property_id": properties[0]["_id"],
        "url": "https://example.com/image2.jpg",
        "caption": "Master bedroom",
        "is_primary": False,
        "created_at": datetime.datetime.utcnow()
    },
    {
        "_id": ObjectId(),
        "property_id": properties[1]["_id"],
        "url": "https://example.com/image3.jpg",
        "caption": "Living room with city view",
        "is_primary": True,
        "created_at": datetime.datetime.utcnow()
    }
]

# Insert sample data into MongoDB collections
db.properties.insert_many(properties)
db.property_attributes.insert_many(attributes)
db.property_images.insert_many(images)

print("Sample data inserted successfully!")

# Close the MongoDB connection
client.close()