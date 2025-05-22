import tkinter as tk
from tkinter import ttk


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("kalkulator")
        self.geometry("300x250")
        self.num1 = tk.StringVar()
        self.num2 = tk.StringVar()
        self.result = tk.StringVar()

        ttk.Label(self, text="angka 1").grid(
            row=0, column=0, padx=(10, 5), pady=(10, 5))
        ttk.Label(self, text="angka 2").grid(
            row=1, column=0, padx=(10, 5), pady=(10, 5))
        ttk.Label(self, text="hasil").grid(
            row=2, column=0, padx=(10, 5), pady=(10, 5))

        ent_num = ttk.Entry(self, textvariable=self.num1).grid(
            row=0, column=1, padx=(5, 10), pady=(10, 5))
        ent_num = ttk.Entry(self, textvariable=self.num2).grid(
            row=1, column=1, padx=(5, 10), pady=(10, 5))
        ent_num = ttk.Entry(self, textvariable=self.result).grid(
            row=2, column=1, padx=(5, 10), pady=(10, 5))

        btn_sub = ttk.Button(
            self, text="+", command=self.sub).grid(row=3, column=0, padx=(10, 5), pady=(10, 5))
        btn_min = ttk.Button(
            self, text="-", command=self.min).grid(row=4, column=0, padx=(10, 5), pady=(10, 5))
        btn_kali = ttk.Button(
            self, text="*", command=self.kal).grid(row=3, column=1, padx=(5, 10), pady=(10, 5))
        btn_bagi = ttk.Button(
            self, text="/", command=self.bagi).grid(row=4, column=1, padx=(5, 10), pady=(10, 5))

    def sub(self):
        try:
            self.result.set(
                str(float(self.num1.get()) + float(self.num2.get())))
        except ValueError:
            self.result.set("Input salah")

    def min(self):
        try:
            self.result.set(
                str(float(self.num1.get()) - float(self.num2.get())))
        except ValueError:
            self.result.set("Input salah")

    def kal(self):
        try:
            self.result.set(str(float(self.num1.get())
                            * float(self.num2.get())))
        except ValueError:
            self.result.set("Input salah")

    def bagi(self):
        try:
            if float(self.num2.get()) != 0:
                result = float(self.num1.get()) / float(self.num2.get())
                self.result.set(str(result))
            else:
                self.result.set("Tidak bisa dibagi 0")
        except ValueError:
            self.result.set("Input salah")


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
