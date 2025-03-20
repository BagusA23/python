class Book:
    id = 1

    def __init__(self, title: str, author: str, isbn: str, price: int, pages: int, publisher: str = "gramedia"):
        self.title = title  # nama produk
        self.author = author  # nama pembuat
        self.isbn = isbn  # kode unik
        self.price = price  # harga
        self.pages = pages  # total halaman
        self.publisher = publisher  # penerbit
        self.id = Book.id #memanggill variable id yang sudah ada di class Book
        Book.id += 1 #mengupdate nilai id

    def display_info(self) -> None:
        info = (
            f"ID         : {self.id}\n"
            f"Title      : {self.title}\n"
            f"Author     : {self.author}\n"
            f"ISBN       : {self.isbn}\n"
            f"Price      : Rp.{self.price:,}\n"
            f"Pages      : {self.pages} pages\n"
            f"Publisher  : {self.publisher}\n"
        )
        print(info)


# Membuat objek Book
book1 = Book("Malin Kundang", "Rendra", "123456789", 20000, 200)
book2 = Book("Kemana dirimu", "Cecep", "123456789", 18000, 20, "erlangga")
book3 = Book("Dunia Berputar", "Albert", "123456789", 200000, 100, "airalang")


# Menampilkan informasi buku
book1.display_info()
book2.display_info()
book3.display_info()
