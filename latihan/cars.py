class Car:
    id_counter = 1

    def __init__(self, brand: str, model: str, year: int, price: int, fuel_type: str = "Bensin"):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.fuel_type = fuel_type
        self.id = Car.id_counter
        Car.id_counter += 1

    def display_info(self) -> None:
        info = (
            f"ID        : {self.id}\n"
            f"Brand     : {self.brand.capitalize()}\n"
            f"Model     : {self.model.capitalize()}\n"
            f"Year      : {self.year}\n"
            f"Price     : Rp{self.price:,}\n"
            f"Fuel Type : {self.fuel_type.capitalize()}\n"
        )
        print(info)


# Membuat instance dari class Car
car1 = Car("toyota", "fortuner", 2016, 300000000, "diesel")
car2 = Car("toyota", "avanza", 2016, 100000000)

# Menampilkan informasi mobil
car1.display_info()
car2.display_info()
