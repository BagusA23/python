class SimpleCalculator:
    def __init__(self, input_pertama, input_kedua):
        self.pertama = input_pertama
        self.kedua = input_kedua

    def tambah(self):
        return self.pertama + self.kedua

    def kurang(self):
        return self.pertama - self.kedua

    def kali(self):
        return self.pertama * self.kedua

    def bagi(self):
        if self.kedua != 0 or self.pertama != 0:
            return self.pertama / self.kedua
        else:
            raise ValueError("Tidak bisa melakukan pembagian dengan angka 0.")

    def __str__(self):
        return f"Calculator dengan input pertama {self.pertama} dan input kedua {self.kedua}"

    def hasil(self, operasi):
        operasi_dict = {
            "tambah": self.tambah,
            "kurang": self.kurang,
            "kali": self.kali,
            "bagi": self.bagi,
            "+": self.tambah,
            "-": self.kurang,
            "*": self.kali,
            "/": self.bagi
        }
        return operasi_dict.get(operasi, lambda: "Operasi tidak valid")()


inputsatu = int(input("Masukan angka pertama: "))
inputdua = int(input("Masukan angka kedua: "))
calculator = SimpleCalculator(inputsatu, inputdua)
print(calculator)
operasi = input("Masukan operasi (+, -, *, /): ")
try:
    print(calculator.hasil(operasi))
except ValueError as e:
    print(e)


class ExtraCalculator(SimpleCalculator):
    def tambah(self):
        return self.pertama + self.kedua + 10
    
