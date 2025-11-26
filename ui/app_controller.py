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
        self.current_frame = None      # stores the page currently displayed
        self.user = None               # stores logged-in user object
        self.show_login()              # first screen to display

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()   # remove previous page from window
            self.current_frame = None

    def show_login(self):
        self.clear()
        self.current_frame = LoginPage(self.root, controller=self)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self, user):
        self.user = user                  # keep track of logged-in user
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
        self.user = None                  # remove user session on logout
        self.show_login()                 # return to login page
