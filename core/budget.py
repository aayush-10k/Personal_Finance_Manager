# core/budget.py
from dataclasses import dataclass, field
import uuid

@dataclass
class Budget:
    category: str
    amount: float
    month: str  # format: YYYY-MM (budget applies to a specific month)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # auto-generate unique budget ID
