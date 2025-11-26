# ui/register_page.py
import tkinter as tk
from tkinter import messagebox
from storage.storage_manager import StorageManager
from utils.password_hasher import PasswordHasher
from core.user import User, UserProfile

class RegisterPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.sm = StorageManager()          # handles saving/loading users from storage
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Register", font=("Helvetica", 18, "bold")).pack(pady=10)
        frm = tk.Frame(self); frm.pack(pady=5)
        tk.Label(frm, text="Username").grid(row=0,column=0, sticky="e")
        tk.Label(frm, text="Password").grid(row=1,column=0, sticky="e")
        tk.Label(frm, text="Full Name").grid(row=2,column=0, sticky="e")
        self.username = tk.Entry(frm); self.username.grid(row=0,column=1, padx=5, pady=4)
        self.password = tk.Entry(frm, show="*"); self.password.grid(row=1,column=1, padx=5, pady=4)
        self.fullname = tk.Entry(frm); self.fullname.grid(row=2,column=1, padx=5, pady=4)

        btn_frame = tk.Frame(self); btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create Account", command=self.register).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back to Login", command=self.back_to_login).pack(side="left", padx=5)

    def register(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        name = self.fullname.get().strip() or uname   # if full name empty, use username instead
        if not uname or not pwd:
            messagebox.showerror("Error", "Enter username and password")
            return

        users = self.sm.load_users()
        if any(u.username == uname for u in users):   # prevents duplicate usernames
            messagebox.showerror("Error", "Username already exists")
            return

        ph = PasswordHasher.hash_password(pwd)        # convert password → hashed password
        profile = UserProfile(name=name)
        u = User(uname, ph, profile)                  # create new user object
        users.append(u)
        self.sm.save_users(users)                     # save updated list to storage

        messagebox.showinfo("Success", "Registered successfully. Please login.")
        self.back_to_login()                          # after registration, go back to login page

    def back_to_login(self):
        self.controller.show_login()                  # switch screen to login
