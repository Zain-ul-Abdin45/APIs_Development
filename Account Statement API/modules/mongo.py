import pymongo
import json
from typing import List, Dict, Optional

class MongoClient:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = json.load(file)
        self.client = pymongo.MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]

    def get_account_details(self, collection_name: str, account_id: str) -> Optional[Dict]:
        """
        Retrieve account details from MongoDB by account_id.
        """
        collection = self.db[collection_name]
        account_details = collection.find_one({"account_id": account_id})
        return account_details

    def get_transactions(self, collection_name: str, account_id: str, start_date: str, end_date: str, limit: int = 5000) -> List[Dict]:
        """
        Retrieve transactions based on account_id and date range, with a configurable limit.
        """
        collection = self.db[collection_name]
        transactions = collection.find({
            "account_id": account_id,
            "date": {"$gte": start_date, "$lte": end_date}
        }).sort("date", pymongo.DESCENDING).limit(limit)
        
        return list(transactions)

    def store_response(self, collection_name: str, response_data: Dict):
        """
        Store the final merged result into the response collection.
        """
        collection = self.db[collection_name]
        collection.insert_one(response_data)
