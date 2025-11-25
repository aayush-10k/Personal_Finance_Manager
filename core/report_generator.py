# core/report_generator.py
from typing import List
from core.transaction import Transaction
from collections import defaultdict
import datetime

class ReportGenerator:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions

    def monthly_summary(self, year: int, month: int):
        by_cat = defaultdict(float)
        total_income = 0.0
        total_expense = 0.0

        for t in self.transactions:
            try:
                dt = datetime.datetime.fromisoformat(t.date)
            except Exception:
                dt = datetime.datetime.now()

            if dt.year == year and dt.month == month:

                # EXPENSE → store as negative
                if t.ttype == "expense":
                    total_expense += t.amount
                    by_cat[t.category] -= t.amount

                # INCOME → store as positive
                else:
                    total_income += t.amount
                    by_cat[t.category] += t.amount

        return {
            "income": total_income,
            "expense": total_expense,
            "by_category": dict(by_cat)
        }
