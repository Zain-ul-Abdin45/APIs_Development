from typing import List, Dict
from .mongo import MongoClient
from .cleaner import Cleaner
from .models import TransactionQueryModel

class Worker:
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client
        self.cleaner = Cleaner(mongo_client)

    def fetch_and_process_transactions(self, query_data: TransactionQueryModel) -> Dict:
        """
        Fetches account details and transactions, merges the data, and stores it in the response collection.
        """
        # Fetch account details
        account_details = self.mongo_client.get_account_details("account_details", query_data.account_id)
        if not account_details:
            raise ValueError(f"Account with ID {query_data.account_id} not found.")

        # Fetch transactions
        transactions = self.mongo_client.get_transactions(
            "transactions",
            query_data.account_id,
            query_data.start_date,
            query_data.end_date,
            query_data.limit
        )

        # Merge account details and transactions
        response_data = {
            "account_details": account_details,
            "transactions": transactions,
            "query": query_data.dict(),
            "timestamp": int(time.time())  # Store timestamp for cleaner
        }

        # Store the merged response in the response collection
        self.mongo_client.store_response("response", response_data)

        # Clean old cached data
        self.cleaner.clean_cached_data("response")

        return response_data
