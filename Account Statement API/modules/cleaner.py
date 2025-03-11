from typing import List, Dict

class Cleaner:
    @staticmethod
    def clean_transactions(transactions: List[Dict]) -> List[Dict]:
        """
        Cleans and formats the transaction data.
        Example: Removing sensitive information or adjusting date formats.
        """
        cleaned_transactions = []
        for transaction in transactions:
            cleaned_transaction = {
                "transaction_id": transaction.get("transaction_id"),
                "amount": transaction.get("amount"),
                "date": transaction.get("date"),
                "description": transaction.get("description", "No description available")
            }
            cleaned_transactions.append(cleaned_transaction)
        return cleaned_transactions
