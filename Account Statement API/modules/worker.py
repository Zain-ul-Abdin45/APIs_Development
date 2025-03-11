from typing import List, Dict
from .mongo import MongoClient
from .cleaner import Cleaner

class Worker:
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    def fetch_and_process_transactions(self, collection_name: str, limit: int = 3500) -> List[Dict]:
        """
        Fetches transactions from MongoDB, processes them, and limits the number of transactions to the required maximum.
        """
        transactions = self.mongo_client.get_transactions(collection_name)
        
        # Limit the number of transactions if there are more than the threshold
        if len(transactions) > limit:
            transactions = transactions[:limit]

        # Clean and format transactions
        cleaned_transactions = Cleaner.clean_transactions(transactions)
        
        return cleaned_transactions
