# core/budget.py
from dataclasses import dataclass, field
import uuid

@dataclass
class Budget:
    category: str
    amount: float
    month: str  # 'YYYY-MM'
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
