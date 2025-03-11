import pymongo
import json
from typing import List, Dict

class MongoClient:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = json.load(file)
        self.client = pymongo.MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]

    def get_transactions(self, collection_name: str, limit: int = None) -> List[Dict]:
        """
        Retrieves transactions from the specified MongoDB collection,
        sorted by descending date, with an optional limit.
        """
        collection = self.db[collection_name]
        if limit:
            return list(collection.find().sort('date', pymongo.DESCENDING).limit(limit))
        return list(collection.find().sort('date', pymongo.DESCENDING))
