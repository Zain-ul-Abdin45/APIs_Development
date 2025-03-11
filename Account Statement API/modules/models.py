from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from typing import Optional

class TransactionQueryModel(BaseModel):
    account_id: str
    start_date: str
    end_date: str
    limit: Optional[int] = 5000  # Default to 5000 if not provided

    @validator('start_date', 'end_date')
    def check_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
        return v

    @validator('end_date')
    def check_date_range(cls, v, values):
        start_date = values.get('start_date')
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(v, '%Y-%m-%d')
        
        # Check if the end date is not more than 2 years ahead of the start date
        if (end_dt - start_dt).days > 730:  # 730 days = 2 years
            raise ValueError("Date range cannot exceed 2 years.")
        if end_dt < start_dt:
            raise ValueError("End date cannot be earlier than start date.")
        return v
