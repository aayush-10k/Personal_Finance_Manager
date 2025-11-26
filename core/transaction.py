# core/transaction.py
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Transaction:
    amount: float
    category: str
    ttype: str  # 'expense' or 'income'
    note: str = ""
    date: str = field(default_factory=lambda: datetime.now().isoformat())  # auto-store timestamp in ISO format
    id: str = field(default_factory=lambda: str(uuid.uuid4()))             # unique transaction ID

    @property
    def signed_amount(self):
        # expense = negative amount, income = positive amount
        return -self.amount if self.ttype == "expense" else self.amount
