class Student:
    def __init__(self, name: str, age: int, npm: int, prodi: str):
        self.npm = npm
        self.name = name
        self.age = age
        self.prodi = prodi

    def infor(self) -> None:
        print(f"Nama : {self.name}")
        print(f"Umur : {self.age} tahun")
        print(f"NPM : {self.npm}")
        print(f"Prodi : {self.prodi}")


p1 = Student('Bagus', 12, 12, 'Informatika')
p1.infor()

p1.age = 20
p1.name = 'Bagus Satria'
p1.infor()
