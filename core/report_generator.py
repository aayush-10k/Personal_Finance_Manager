# core/report_generator.py
from typing import List
from core.transaction import Transaction
from collections import defaultdict
import datetime

class ReportGenerator:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions   # list of all transactions for a user

    def monthly_summary(self, year: int, month: int):
        by_cat = defaultdict(float)       # category → total amount
        total_income = 0.0
        total_expense = 0.0

        for t in self.transactions:
            try:
                dt = datetime.datetime.fromisoformat(t.date)   # convert stored string to datetime
            except Exception:
                dt = datetime.datetime.now()                  # fallback if format is invalid

            # consider only transactions of selected month & year
            if dt.year == year and dt.month == month:

                # EXPENSE stored as negative in category breakdown
                if t.ttype == "expense":
                    total_expense += t.amount
                    by_cat[t.category] -= t.amount

                # INCOME stored as positive
                else:
                    total_income += t.amount
                    by_cat[t.category] += t.amount

        return {
            "income": total_income,
            "expense": total_expense,
            "by_category": dict(by_cat)   # convert defaultdict → normal dict
        }
