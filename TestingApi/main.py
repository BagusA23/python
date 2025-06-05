import tkinter as tk
from tkinter import ttk
from product_ui import ProductUI
from user_ui import UserUI

root = tk.Tk()
root.title("Go API Client - Product & User Manager")

tab_control = tk.ttk.Notebook(root)

product_tab = tk.Frame(tab_control)
user_tab = tk.Frame(tab_control)

tab_control.add(product_tab, text="Products")
tab_control.add(user_tab, text="Users")


tab_control.pack(expand=1, fill="both")

ProductUI(product_tab)
UserUI(user_tab)

root.mainloop()
