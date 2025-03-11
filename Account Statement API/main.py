from fastapi import FastAPI, HTTPException
from typing import List, Dict
from module.mongo import MongoClient
from module.worker import Worker
import json

app = FastAPI()

# Initialize MongoDB client and worker
mongo_client = MongoClient('configs/mongodb.json')
worker = Worker(mongo_client)

@app.get("/transactions", response_model=List[Dict])
async def get_transactions():
    """
    Endpoint to fetch the transaction history.
    Returns the latest 3500 transactions if available, or fewer if there are less than 3500.
    """
    try:
        # Fetch and process transactions
        transactions = worker.fetch_and_process_transactions("transactions", limit=3500)
        
        # If no transactions are found, return an empty list
        if not transactions:
            return []
        
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

