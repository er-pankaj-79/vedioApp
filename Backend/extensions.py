from pymongo import MongoClient
import os

client = None
db = None

def init_db():
    global client, db
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
