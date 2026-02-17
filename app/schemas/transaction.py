from pydantic import BaseModel
from typing import Optional

class TransactionOutput(BaseModel):
    date: Optional[str]
    libelle: str
    tiers: str
    debit: str
    credit: str
    montant: float

class ReconciliationResult(BaseModel):
    filename: str
    transactions: list[TransactionOutput]
