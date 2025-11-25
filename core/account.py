# core/account.py
from dataclasses import dataclass, field
from typing import List
import uuid
from core.transaction import Transaction

@dataclass
class Account:
    name: str
    account_type: str = "wallet"  # wallet, bank, card
    balance: float = 0.0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, tx: Transaction):
        self.transactions.append(tx)
        self.balance += tx.signed_amount
