# ui/components/custom_widgets.py
import tkinter as tk

class LabeledEntry(tk.Frame):
    def __init__(self, master, label, **opts):
        super().__init__(master, **opts)
        self.lbl = tk.Label(self, text=label, anchor="w")   # text label above input
        self.entry = tk.Entry(self)                         # input box
        self.lbl.pack(fill="x")
        self.entry.pack(fill="x")

    def get(self):
        return self.entry.get()                             # return text entered

    def set(self, v):
        self.entry.delete(0, "end")                         # clear existing value
        self.entry.insert(0, v)                             # set new value
