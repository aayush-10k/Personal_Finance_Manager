# ui/add_transaction_page.py
import tkinter as tk
from tkinter import messagebox
from storage.storage_manager import StorageManager
from core.transaction import Transaction
from core.category import EXPENSE_CATEGORIES, INCOME_CATEGORIES


class AddTransactionPage(tk.Frame):
    def __init__(self, master, controller, user):
        super().__init__(master)
        self.controller = controller
        self.user = user
        self.sm = StorageManager()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Add Transaction", font=("Helvetica", 16, "bold")).pack(pady=10)

        frm = tk.Frame(self)
        frm.pack(pady=6)

        tk.Label(frm, text="Amount").grid(row=0, column=0, sticky="e")
        tk.Label(frm, text="Type").grid(row=1, column=0, sticky="e")
        tk.Label(frm, text="Category").grid(row=2, column=0, sticky="e")
        tk.Label(frm, text="Note").grid(row=3, column=0, sticky="e")

        self.amount = tk.Entry(frm)
        self.amount.grid(row=0, column=1, padx=6, pady=4)

        # dropdown to choose income/expense
        self.ttype = tk.StringVar(value="expense")
        type_menu = tk.OptionMenu(frm, self.ttype, "expense", "income", command=self.update_categories)
        type_menu.grid(row=1, column=1, padx=6, pady=4)

        # category list changes depending on income/expense
        self.category_var = tk.StringVar()
        self.category_menu = tk.OptionMenu(frm, self.category_var, *EXPENSE_CATEGORIES.keys())
        self.category_var.set("🍔 Food")
        self.category_menu.grid(row=2, column=1, padx=6, pady=4)

        self.note = tk.Entry(frm)
        self.note.grid(row=3, column=1, padx=6, pady=4)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        tk.Button(btns, text="Save", width=12, command=self.save).pack(side="left", padx=6)
        tk.Button(btns, text="Back", width=12, command=lambda: self.controller.show_dashboard(self.user)).pack(side="left", padx=6)

    def update_categories(self, choice):
        """ Change dropdown items dynamically based on type """

        menu = self.category_menu["menu"]
        menu.delete(0, "end")   # clear old category options

        # choose income or expense category list
        if self.ttype.get() == "expense":
            categories = EXPENSE_CATEGORIES
        else:
            categories = INCOME_CATEGORIES

        for icon_label in categories.keys():      # rebuild dropdown menu items
            menu.add_command(label=icon_label, command=lambda v=icon_label: self.category_var.set(v))

        first_key = list(categories.keys())[0]    # set first item as default
        self.category_var.set(first_key)

    def save(self):
        try:
            amt = float(self.amount.get())        # convert string amount → number
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        # Extract category name (without emoji/icon)
        cat_with_icon = self.category_var.get()
        if self.ttype.get() == "expense":
            category = EXPENSE_CATEGORIES[cat_with_icon]
        else:
            category = INCOME_CATEGORIES[cat_with_icon]

        # create Transaction object for saving
        tx = Transaction(
            amount=amt,
            category=category,
            ttype=self.ttype.get(),
            note=self.note.get() or ""
        )

        txs = self.sm.load_transactions(self.user.id)  # load user's previous transactions
        txs.append(tx)                                 # add new transaction
        self.sm.save_transactions(self.user.id, txs)   # save back to file/storage

        messagebox.showinfo("Success", "Transaction saved")
        self.controller.show_dashboard(self.user)      # navigate back to dashboard
