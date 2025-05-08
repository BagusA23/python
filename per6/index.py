import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Halo Dunia")
root.geometry("500x300")

student = tk.StringVar()


def hello():
    nama = student.get()
    if nama:
        messagebox.showinfo("Halo", f"Halo {nama}")
    else:
        messagebox.showerror("Error", "Please enter your name")


nama = ttk.Label(root, text="Nama:")
nama.pack(side="left", padx=(5, 10), pady=(10, 10))

ent_nama = ttk.Entry(root, textvariable=student)
ent_nama.pack(side="left", padx=(5, 10), pady=(10, 10))
ent_nama.focus()

btn_test = ttk.Button(root, text="Hello", command=hello)
btn_test.pack(side="left", padx=(5, 10))

btn_close = ttk.Button(root, text="Close", command=root.destroy)
btn_close.pack(side="left", padx=(5, 10))

root.mainloop()