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
    date: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def signed_amount(self):
        return -self.amount if self.ttype == "expense" else self.amount
