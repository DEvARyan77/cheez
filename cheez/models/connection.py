from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user']
    collection = db['users']
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB:")