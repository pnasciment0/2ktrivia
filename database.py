from pymongo import MongoClient
import os

class MongoDBHandler:
    def __init__(self, mongo_db=None, mongo_collection=None):
        # If parameters are not provided, fall back to environment variables
        self.mongo_uri = os.getenv('MONGO_URI')
        self.mongo_db = mongo_db if mongo_db else os.getenv('MONGO_DATABASE')
        self.mongo_collection = mongo_collection if mongo_collection else os.getenv('MONGO_COLLECTION')
        
        # Initialize the MongoDB client and select the database and collection
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def insert_record(self, collection_name, record_data):
        collection = self.db[collection_name]
        if not collection.find_one(record_data):
            collection.insert_one(record_data)

    def update_record(self, collection_name, query_criteria, record_data):
        collection = self.db[collection_name]
        collection.update_one(query_criteria, {'$set': record_data}, upsert=True)

    def delete_record(self, collection_name, query_criteria):
        collection = self.db[collection_name]
        collection.delete_one(query_criteria)

    def close(self):
        self.client.close()