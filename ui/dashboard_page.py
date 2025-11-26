# ui/dashboard_page.py
import tkinter as tk
from tkinter import messagebox
from storage.storage_manager import StorageManager
from core.report_generator import ReportGenerator
import datetime

class DashboardPage(tk.Frame):
    def __init__(self, master, controller, user):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.sm = StorageManager()
        self.build_ui()

    def build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=10)

        tk.Label(
            top,
            text=f"Dashboard - {self.user.profile.name or self.user.username}",
            font=("Helvetica", 16, "bold")
        ).pack(side="left", padx=10)

        btns = tk.Frame(top)
        btns.pack(side="right", padx=10)

        tk.Button(btns, text="Add Transaction", command=self.controller.show_add_transaction).pack(side="left", padx=5)
        tk.Button(btns, text="Reports", command=self.controller.show_reports).pack(side="left", padx=5)
        tk.Button(btns, text="Logout", command=self.logout).pack(side="left", padx=5)

        summary_frame = tk.Frame(self, relief="groove", bd=1)
        summary_frame.pack(fill="x", padx=12, pady=12)

        self.summary_label = tk.Label(summary_frame, text="Loading summary...", font=("Helvetica", 12))
        self.summary_label.pack(padx=8, pady=8)

        # frame to show latest transaction list
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, padx=12, pady=6)

        self.update_summary()    # fetch and display summary + recent transactions

    def update_summary(self):
        txs = self.sm.load_transactions(self.user.id)   # get all transactions for logged-in user
        now = datetime.datetime.now()
        rg = ReportGenerator(txs)
        summary = rg.monthly_summary(now.year, now.month)   # summary only for current month

        income = summary["income"]
        expense = summary["expense"]
        net = income - expense

        if net > 0:
            net_text = f"Net Profit: +{net:.2f}"
        else:
            net_text = f"Net Loss: {net:.2f}"

        txt = (
            f"Income: {income:.2f}    "
            f"Expense: {expense:.2f}    "
            f"{net_text}"
        )
        self.summary_label.config(text=txt)

        # clear previously shown list before repopulating
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # show recent 10 transactions (sorted by date)
        txs_sorted = sorted(txs, key=lambda t: t.date, reverse=True)[:10]

        for t in txs_sorted:
            try:
                dt = datetime.datetime.fromisoformat(t.date)
                formatted = dt.strftime("%Y-%m-%d  %I:%M %p")
            except:
                formatted = t.date

            from core.category import EXPENSE_CATEGORIES, INCOME_CATEGORIES

            # reverse mapping to add emojis/icons again
            lookup = {v: k for k, v in EXPENSE_CATEGORIES.items()}
            lookup.update({v: k for k, v in INCOME_CATEGORIES.items()})
            icon = lookup.get(t.category, "")

            line = (
                f"{formatted}  |  {icon} {t.category}  |  "
                f"{t.ttype}  |  {t.amount:.2f}  |  {t.note}"
            )

            tk.Label(self.list_frame, text=line, anchor="w").pack(fill="x")

    def logout(self):
        # confirmation box before logout
        if tk.messagebox.askyesno("Logout", "Do you want to logout?"):
            self.controller.logout()
