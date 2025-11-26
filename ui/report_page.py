# ui/report_page.py
import tkinter as tk
from storage.storage_manager import StorageManager
from core.report_generator import ReportGenerator
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ReportPage(tk.Frame):
    def __init__(self, master, controller, user):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.sm = StorageManager()                  # used to load transactions from storage
        self.build_ui()

    def build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=6)

        tk.Label(top, text="Monthly Report", font=("Helvetica", 16, "bold")).pack(side="left", padx=10)

        tk.Button(
            top,
            text="Back",
            command=lambda: self.controller.show_dashboard(self.user)   # go back to dashboard page
        ).pack(side="right", padx=10)

        now = datetime.datetime.now()
        txs = self.sm.load_transactions(self.user.id)                  # fetch all transactions for user
        rg = ReportGenerator(txs)
        summary = rg.monthly_summary(now.year, now.month)              # get report for current month only

        income = summary["income"]
        expense = summary["expense"]
        net = income - expense

        # display profit or loss status
        if net > 0:
            net_text = f"Net Profit: +{net:.2f}"
        else:
            net_text = f"Net Loss: {net:.2f}"

        tk.Label(
            self,
            text=f"Income: {income:.2f}   Expense: {expense:.2f}   {net_text}",
            font=("Helvetica", 12)
        ).pack(pady=6)

        # Build chart
        cats = list(summary["by_category"].keys())                    # list of categories
        vals = [summary["by_category"][c] for c in cats]              # spending/income per category

        fig, ax = plt.subplots(figsize=(6, 3))

        if cats:
            # income → green  | expense → red
            colors = ["green" if v > 0 else "red" for v in vals]

            ax.bar(cats, vals, color=colors)
            ax.axhline(0, color="black", linewidth=1)                  # baseline at zero
            ax.set_title(f"Category Breakdown for {now.strftime('%B %Y')}")
            ax.set_ylabel("Amount")
            fig.tight_layout()

            # embed matplotlib chart inside Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=8)
            canvas.draw()

        else:
            tk.Label(self, text="No transactions found for this month").pack(pady=20)
