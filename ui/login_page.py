# ui/login_page.py
import tkinter as tk
from tkinter import messagebox
from storage.storage_manager import StorageManager
from utils.password_hasher import PasswordHasher
from core.user import UserProfile, User
from ui.register_page import RegisterPage

class LoginPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.sm = StorageManager()
        self.users = self.sm.load_users()
        self.build_ui()

    def build_ui(self):
        top = tk.Frame(self)
        top.pack(pady=20)
        tk.Label(top, text="Personal Finance Manager", font=("Helvetica", 20, "bold")).pack()

        form = tk.Frame(self)
        form.pack(pady=10)
        tk.Label(form, text="Username").grid(row=0,column=0, sticky="e")
        tk.Label(form, text="Password").grid(row=1,column=0, sticky="e")
        self.username = tk.Entry(form); self.username.grid(row=0,column=1, padx=5, pady=5)
        self.password = tk.Entry(form, show="*"); self.password.grid(row=1,column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self); btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", width=12, command=self.login).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Register", width=12, command=self.open_register).pack(side="left", padx=5)

    def login(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        if not uname or not pwd:
            messagebox.showerror("Error", "Enter username and password")
            return
        self.users = self.sm.load_users()
        for u in self.users:
            if u.username == uname:
                if PasswordHasher.verify(u.password_hash, pwd):
                    messagebox.showinfo("Login", f"Welcome {u.profile.name or u.username}")
                    # navigate to dashboard via controller
                    self.controller.show_dashboard(u)
                    return
                else:
                    messagebox.showerror("Login", "Invalid password")
                    return
        messagebox.showerror("Login", "User not found")

    def open_register(self):
        self.controller.clear()
        self.controller.current_frame = RegisterPage(self.master, controller=self.controller)
        self.controller.current_frame.pack(fill="both", expand=True)

