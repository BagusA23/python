import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:8080/register"
API_URL_LOGIN = "http://localhost:8080/login"


class UserUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Form Entry
        tk.Label(self.frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Add User",
                  command=self.add_user).grid(row=2, columnspan=2)

        # User List
        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack()
        self.refresh_users()

    def add_user(self):
        data = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 200 or response.status_code == 201:
            messagebox.showinfo("Success", "User added successfully!")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "Failed to add user")

    def refresh_users(self):
        self.listbox.delete(0, tk.END)
        response = requests.post(API_URL_LOGIN)
        if response.status_code == 200:
            for user in response.json():
                self.listbox.insert(tk.END, f"Username: {user['username']}")
