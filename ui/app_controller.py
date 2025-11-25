# ui/app_controller.py
import tkinter as tk
from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage
from ui.add_transaction_page import AddTransactionPage
from ui.report_page import ReportPage

class AppController:
    """
    Simple controller to switch between pages.
    Usage: AppController(root)
    """
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.user = None
        self.show_login()

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self):
        self.clear()
        self.current_frame = LoginPage(self.root, controller=self)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self, user):
        self.user = user
        self.clear()
        self.current_frame = DashboardPage(self.root, controller=self, user=user)
        self.current_frame.pack(fill="both", expand=True)

    def show_add_transaction(self):
        self.clear()
        self.current_frame = AddTransactionPage(self.root, controller=self, user=self.user)
        self.current_frame.pack(fill="both", expand=True)

    def show_reports(self):
        self.clear()
        self.current_frame = ReportPage(self.root, controller=self, user=self.user)
        self.current_frame.pack(fill="both", expand=True)

    def logout(self):
        self.user = None
        self.show_login()
