class Product:
    def __init__(self, nama: str, merek: str, deskripsi: str, harga: int, stok: int, kategori: str):
        self.nama = nama
        self.merek = merek
        self.deskripsi = deskripsi
        self.harga = harga
        self.stok = stok
        self.kategori = kategori

    def display_info(self) -> None:
        info = (
            f"Nama      : {self.nama.capitalize()}\n"
            f"Merek     : {self.merek.capitalize()}\n"
            f"Deskripsi : {self.deskripsi}\n"
            f"Harga     : Rp{self.harga:,}\n"
            f"Stok      : {self.stok}\n"
            f"Kategori  : {self.kategori.capitalize()}"
        )
        print(info)


# Membuat instance dari class Product
product1 = Product("laptop gaming", "lenovo",
                   "Ini adalah laptop gaming", 15000000, 5, "teknologi")

# Menampilkan informasi produk
product1.display_info()