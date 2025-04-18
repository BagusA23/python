import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()
root.title("siapp membantai")
root.geometry("300x200")

text_area = ScrolledText(root, undo=True, width=40, height=10)
text_area.pack(fill=tk.BOTH, expand=1)

label = tk.Label(root, text="Hello, world!")
label.pack()

e_los = ttk.Entry(root)
e_los.pack()

root.mainloop()
