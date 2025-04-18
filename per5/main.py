import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText


class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Untitled - Notepad")
        self.geometry("800x600")
        self.file_path = None

        # Membuat Text Area dengan Scroll
        self.text_area = ScrolledText(self, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        # Membuat Menu
        self._create_menu()

        # Menambahkan Shortcut Keyboard
        self._bind_shortcuts()

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(
            label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(
            label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(
            label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate(
            "<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate(
            "<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate(
            "<<Paste>>"), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.event_generate(
            "<<SelectAll>>"), accelerator="Ctrl+A")

        # view menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Show/Hide Scrollbar",
                              command=self.show_hide_scrollbar)

    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda event: self.new_file())
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-a>",
                  lambda event: self.text_area.event_generate("<<SelectAll>>"))
        self.bind("<Control-z>", lambda event: self.text_area.edit_undo())
        self.bind("<Control-y>", lambda event: self.text_area.edit_redo())

    def new_file(self):
        self.file_path = None
        self.text_area.delete("1.0", tk.END)
        self.title("Untitled - Notepad")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
                self.file_path = file_path
                self.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membuka file:\n{e}")

    def save_file(self):
        if self.file_path:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.title(f"{self.file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.file_path = file_path
                self.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file:\n{e}")

    def show_hide_scrollbar(self):
        if self.text_area.vbar.winfo_ismapped():
            self.text_area.vbar.pack_forget()
        else:
            self.text_area.vbar.pack(side=tk.RIGHT, fill=tk.Y)


if __name__ == "__main__":
    app = Notepad()
    app.mainloop()
