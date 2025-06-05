import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:8080/products"


class ProductUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Form Entry
        tk.Label(self.frame, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Category ID").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Price").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.frame)
        self.price_entry.grid(row=2, column=1)

        tk.Button(self.frame, text="Add Product", command=self.add_product).grid(
            row=3, column=0, columnspan=2)
        tk.Button(self.frame, text="Edit Product", command=self.edit_product).grid(
            row=4, column=0, columnspan=2)
        tk.Button(self.frame, text="Delete Product", command=self.delete_product).grid(
            row=5, column=0, columnspan=2)

        # Product List
        self.listbox = tk.Listbox(master, width=60)
        self.listbox.pack()

        # Untuk menyimpan list produk (termasuk id)
        self.products = []

        self.refresh_products()

    def add_product(self):
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Harga harus berupa angka.")
            return

        data = {
            "name": self.name_entry.get(),
            "category_id": self.category_entry.get(),
            "price": price
        }

        response = requests.post(API_URL, json=data)

        if response.status_code in [200, 201]:
            messagebox.showinfo("Success", "Product added successfully!")
            self.refresh_products()
        else:
            messagebox.showerror(
                "Error", f"Failed to add product: {response.text}")

    def refresh_products(self):
        self.listbox.delete(0, tk.END)
        response = requests.get(API_URL)
        self.products = []

        if response.status_code == 200:
            for prod in response.json():
                self.products.append(prod)
                display = f"{prod['name']} | Category: {prod['category_id']} | Price: {prod['price']}"
                self.listbox.insert(tk.END, display)

    def get_selected_product_id(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return None
        return self.products[selected_index[0]]['id']

    def edit_product(self):
        product_id = self.get_selected_product_id()
        if not product_id:
            messagebox.showwarning(
                "No selection", "Pilih produk yang ingin diedit")
            return

        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Harga harus berupa angka.")
            return

        data = {
            "name": self.name_entry.get(),
            "category_id": self.category_entry.get(),
            "price": price
        }

        response = requests.put(f"{API_URL}/{product_id}", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Produk berhasil diedit!")
            self.refresh_products()
        else:
            messagebox.showerror(
                "Error", f"Gagal mengedit produk: {response.text}")

    def delete_product(self):
        product_id = self.get_selected_product_id()
        if not product_id:
            messagebox.showwarning(
                "No selection", "Pilih produk yang ingin dihapus")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Yakin ingin menghapus produk ini?")
        if not confirm:
            return

        response = requests.delete(f"{API_URL}/{product_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Produk berhasil dihapus!")
            self.refresh_products()
        else:
            messagebox.showerror(
                "Error", f"Gagal menghapus produk: {response.text}")
