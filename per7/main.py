import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Kalkulator Modern")
        self.root.geometry("350x300")
        self.root.configure(bg="#495696")  # Background gelap elegan

        self.angka1 = tk.StringVar()
        self.angka2 = tk.StringVar()
        self.result = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#495696",
                        foreground="#ecf0f1", font=("Segoe UI", 11))
        style.configure("TEntry",  Background="#BF9675", font=("Segoe UI", 11))
        style.configure("TButton",
                        background="#BF9675",
                        foreground="black",
                        font=("Segoe UI", 11, "bold"),
                        padding=6)
        style.map("TButton",
                  background=[("active", "#A47551"), ("pressed", "#8B5E3C")],
                  foreground=[("pressed", "white"), ("active", "white")])

        title = ttk.Label(self.root, text="Kalkulator Sederhana",
                          font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        ttk.Label(self.root, text="Angka 1").grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_angka1 = ttk.Entry(
            self.root, textvariable=self.angka1, width=25)
        self.ent_angka1.grid(row=1, column=1, padx=10, pady=5)
        self.ent_angka1.focus()

        ttk.Label(self.root, text="Angka 2").grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        self.ent_angka2 = ttk.Entry(
            self.root, textvariable=self.angka2, width=25)
        self.ent_angka2.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Hasil").grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        self.ent_result = ttk.Entry(
            self.root, textvariable=self.result, width=25, state="readonly")
        self.ent_result.grid(row=3, column=1, padx=10, pady=5)

        # Tombol operasi
        btn_frame = tk.Frame(self.root, bg="#495696")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="+", width=6,
                   command=self.add).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="-", width=6,
                   command=self.subtract).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="×", width=6, command=self.kali).grid(
            row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="÷", width=6, command=self.bagi).grid(
            row=0, column=3, padx=5)

    def add(self):
        try:
            result = float(self.angka1.get()) + float(self.angka2.get())
            self.result.set(str(result))
        except ValueError:
            self.result.set("Input salah")

    def subtract(self):
        try:
            result = float(self.angka1.get()) - float(self.angka2.get())
            self.result.set(str(result))
        except ValueError:
            self.result.set("Input salah")

    def kali(self):
        try:
            result = float(self.angka1.get()) * float(self.angka2.get())
            self.result.set(str(result))
        except ValueError:
            self.result.set("Input salah")

    def bagi(self):
        try:
            if float(self.angka2.get()) != 0:
                result = float(self.angka1.get()) / float(self.angka2.get())
                self.result.set(str(result))
            else:
                self.result.set("Tidak bisa dibagi 0")
        except ValueError:
            self.result.set("Input salah")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
