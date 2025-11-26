# main.py
from ui.app_controller import AppController
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Personal Finance Manager")
    root.geometry("1000x650")
    AppController(root)          # Hand over control of UI to AppController (decides which screen to show)
    root.mainloop()              # Tkinter event loop → keeps the window running

if __name__ == "__main__":       # Ensures main() runs only when file is executed directly
    main()
