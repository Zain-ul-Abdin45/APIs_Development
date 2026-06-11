import time
from module.mongo import MongoClient

class Cleaner:
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    def clean_cached_data(self, collection_name: str):
        """
        Cleans cached data from the response collection every 10 minutes.
        """
        current_time = int(time.time())
        ten_minutes_ago = current_time - 600  # 600 seconds = 10 minutes
        self.mongo_client.db[collection_name].delete_many({"timestamp": {"$lt": ten_minutes_ago}})
