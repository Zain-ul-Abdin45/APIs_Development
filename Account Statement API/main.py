from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from module.mongo import MongoClient
from module.worker import Worker
from module.models import TransactionQueryModel
import json

app = FastAPI()

# Initialize MongoDB client and worker
mongo_client = MongoClient('configs/mongodb.json')
worker = Worker(mongo_client)

@app.post("/transactions", response_model=Dict)
async def get_transactions(query: TransactionQueryModel):
    """
    Endpoint to fetch the transaction history, ensuring proper validation of start_date and end_date.
    """
    try:
        # Fetch and process transactions
        response_data = worker.fetch_and_process_transactions(query)
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
