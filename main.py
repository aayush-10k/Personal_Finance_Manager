# main.py
from ui.app_controller import AppController
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Personal Finance Manager")
    root.geometry("1000x650")
    AppController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
