import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext


class CovidHospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencarian Rumah Sakit COVID-19")
        self.root.geometry("600x500")

        self.setup_ui()

    def setup_ui(self):
        # Label
        self.label = tk.Label(
            self.root, text="Masukkan Wilayah (contoh: Palembang):")
        self.label.pack(pady=10)

        # Entry
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack()

        # Tombol cari
        self.search_button = tk.Button(
            self.root, text="Cari Rumah Sakit", command=self.search_hospitals)
        self.search_button.pack(pady=10)

        # Area hasil
        self.result_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=70, height=20)
        self.result_area.pack(pady=10)

    def search_hospitals(self):
        region_query = self.entry.get().strip().upper()

        if not region_query:
            messagebox.showwarning(
                "Peringatan", "Silakan masukkan nama wilayah.")
            return

        try:
            url = 'https://raw.githubusercontent.com/lakuapik/jadwalsholatorg/master/kota.json'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                self.result_area.delete(1.0, tk.END)

                ditemukan = False
                for rs in data:
                    if region_query in rs['region'].upper():
                        ditemukan = True
                        hasil = (
                            f"Nama RS  : {rs['name']}\n"
                            f"Region   : {rs['region']}\n"
                            f"Alamat   : {rs['address']}\n"
                            f"Telepon  : {rs['phone']}\n"
                            + "-" * 50 + "\n"
                        )
                        self.result_area.insert(tk.END, hasil)

                if not ditemukan:
                    self.result_area.insert(
                        tk.END, "Tidak ditemukan rumah sakit di wilayah tersebut.")
            else:
                messagebox.showerror("Error", "Gagal mengambil data dari API.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CovidHospitalApp(root)
    root.mainloop()
