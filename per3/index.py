import math as mt


class Lingkaran:
    def __init__(self, jari_jari):
        if not isinstance(jari_jari, (int, float)) or jari_jari <= 0:
            raise ValueError("Jari-jari harus berupa angka positif")
        self.jari_jari = jari_jari

    def hitung_luas(self):
        return mt.pi * (self.jari_jari ** 2)

    def hitung_keliling(self):
        return 2 * mt.pi * self.jari_jari

    def __str__(self):
        luas = round(self.hitung_luas(), 2)
        keliling = round(self.hitung_keliling(), 2)
        return f"Jari-jari: {self.jari_jari} cm\nLuas: {luas} cm^2\nKeliling: {keliling} cm"


def main():
    while True:
        try:
            jari_jari = float(input("Masukan jari-jari lingkaran: "))
            oop = Lingkaran(jari_jari)
            print(oop)
            break
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
