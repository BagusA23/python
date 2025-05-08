import tkinter as tk
from tkinter import ttk, messagebox


class SayHello:
    def __init__(self, root):
        self.root = root
        self.root.title("SayHello")
        self.root.geometry("400x100")

        self.student = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        nama_label = ttk.Label(self.root, text="Nama:")
        nama_label.pack(side="left", padx=(5, 10), pady=(10, 10))

        self.ent_nama = ttk.Entry(self.root, textvariable=self.student)
        self.ent_nama.pack(side="left", padx=(5, 10), pady=(10, 10))
        self.ent_nama.focus()

        btn_test = ttk.Button(self.root, text="Hello", command=self.hello)
        btn_test.pack(side="left", padx=(5, 10))

        btn_close = ttk.Button(self.root, text="Close",
                               command=self.root.destroy)
        btn_close.pack(side="left", padx=(5, 10))

    def hello(self):
        nama = self.student.get()
        if nama:
            messagebox.showinfo("Halo", f"Halo {nama}")
        else:
            messagebox.showerror("Error", "Please enter your name")


if __name__ == "__main__":
    root = tk.Tk()
    app = SayHello(root)
    root.mainloop()
