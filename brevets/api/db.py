"""
Database insertion and retrieval
"""
from pymongo import MongoClient

class Mongodb:
    def __init__(self, client_name="testclient"):
        self.client_name = client_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.client_name, 27017)

    def set_db(self, db_name):
        self.db = self.client[db_name]

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def list_all_rows(self):
        return list(self.collection.find())

    def find_fields(self, fields):
        fields_dict = {}
        for f in fields:
            fields_dict[f] = 1
        fields_dict["_id"] = 0

        rows = []
        for row in self.collection.find({}, fields_dict):
            rows.append(row)
        return rows

    def find_top_k(self, fields, k):
        fields_dict = {}
        for f in fields:
            fields_dict[f] = 1
        fields_dict["_id"] = 0

        return list(self.collection.find({}, fields_dict).sort("km").limit(k))
