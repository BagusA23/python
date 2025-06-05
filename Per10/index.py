import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:8080/products"


class TreeViewExample(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Product Manager")
        self.geometry("800x600")

        # ========== TREEVIEW ==========
        self.product_tree = ttk.Treeview(self, columns=(
            "id", "name", "category_id", "price"), show='headings')

        self.product_tree.heading("id", text="Product ID")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("category_id", text="Category ID")
        self.product_tree.heading("price", text="Price (Rp.)")

        self.product_tree.column("id", width=80, anchor='center')
        self.product_tree.column("name", anchor="center", width=200)
        self.product_tree.column("category_id", width=100, anchor='center')
        self.product_tree.column("price", width=100, anchor='e')

        self.product_tree.pack(pady=20, fill='x')

        # ========== FORM INPUT ==========
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5)
        tk.Label(form_frame, text="Category ID").grid(row=0, column=1, padx=5)
        tk.Label(form_frame, text="Price").grid(row=0, column=2, padx=5)

        self.name_entry = tk.Entry(form_frame)
        self.category_entry = tk.Entry(form_frame)
        self.price_entry = tk.Entry(form_frame)

        self.name_entry.grid(row=1, column=0, padx=5)
        self.category_entry.grid(row=1, column=1, padx=5)
        self.price_entry.grid(row=1, column=2, padx=5)

        add_button = tk.Button(
            form_frame, text="Add Product", command=self.add_product)
        add_button.grid(row=1, column=3, padx=10)

        edit_button = tk.Button(
            form_frame, text="Edit Product", command=self.edit_product)
        edit_button.grid(row=1, column=4, padx=10)

        self.fetch_products()

    def fetch_products(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                rows = response.json()
                for row in rows:
                    values = (row.get("id"), row.get("name"),
                              row.get("category_id"), row.get("price"))
                    self.product_tree.insert('', 'end', values=values)
            else:
                messagebox.showerror("Error", "Failed to fetch data.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error:\n{e}")

    def add_product(self):
        name = self.name_entry.get()
        category_id = self.category_entry.get()
        price = self.price_entry.get()

        if not name or not category_id or not price:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            payload = {
                "name": name,
                "CategoryID": str(category_id),  # ← Ubah key-nya
                "price": float(price)
            }

            print("Payload:", payload)
            response = requests.post(API_URL, json=payload)
            print("Response:", response.status_code, response.text)

            if response.status_code in (200, 201):
                messagebox.showinfo("Success", "Product added successfully.")
                self.clear_form()
                self.fetch_products()
            else:
                messagebox.showerror(
                    "API Error", f"Failed to add product: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not send data:\n{e}")

    def edit_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Selection Error", "Please select a product to edit.")
            return

        item_values = self.product_tree.item(selected_item, 'values')
        if not item_values:
            messagebox.showwarning("Selection Error", "No product data found.")
            return

        product_id = item_values[0]
        name = self.name_entry.get()
        category_id = self.category_entry.get()
        price = self.price_entry.get()

        if not name or not category_id or not price:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            payload = {
                "id": product_id,
                "name": name,
                "CategoryID": str(category_id),  # ← Ubah key-nya
                "price": float(price)
            }

            response = requests.put(f"{API_URL}/{product_id}", json=payload)

            if response.status_code == 200:
                messagebox.showinfo("Success", "Product updated successfully.")
                self.clear_form()
                self.fetch_products()
            else:
                messagebox.showerror(
                    "API Error", f"Failed to update product: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not send data:\n{e}")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = TreeViewExample()
    app.mainloop()
