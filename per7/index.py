# Konversi dari Tkinter ke Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.17, 0.24, 0.31, 1)  # #2c3e50 background gelap


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        self.angka1 = TextInput(hint_text="Angka 1",
                                multiline=False, font_size=18)
        self.angka2 = TextInput(hint_text="Angka 2",
                                multiline=False, font_size=18)
        self.result = TextInput(hint_text="Hasil", readonly=True, font_size=18)

        self.add_widget(Label(text="Kalkulator Modern",
                        font_size=24, color=(0.93, 0.94, 0.95, 1)))
        self.add_widget(self.angka1)
        self.add_widget(self.angka2)
        self.add_widget(self.result)

        button_layout = BoxLayout(spacing=10, size_hint=(1, 0.3))

        btn_plus = Button(text="+", font_size=20, on_press=self.add)
        btn_min = Button(text="-", font_size=20, on_press=self.subtract)
        btn_mul = Button(text="×", font_size=20, on_press=self.multiply)
        btn_div = Button(text="÷", font_size=20, on_press=self.divide)

        for btn in (btn_plus, btn_min, btn_mul, btn_div):
            button_layout.add_widget(btn)

        self.add_widget(button_layout)

    def get_values(self):
        try:
            a = float(self.angka1.text)
            b = float(self.angka2.text)
            return a, b
        except ValueError:
            self.result.text = "Input salah"
            return None, None

    def add(self, _):
        a, b = self.get_values()
        if a is not None:
            self.result.text = str(a + b)

    def subtract(self, _):
        a, b = self.get_values()
        if a is not None:
            self.result.text = str(a - b)

    def multiply(self, _):
        a, b = self.get_values()
        if a is not None:
            self.result.text = str(a * b)

    def divide(self, _):
        a, b = self.get_values()
        if a is not None:
            if b != 0:
                self.result.text = str(a / b)
            else:
                self.result.text = "Tidak bisa dibagi 0"


class KalkulatorApp(App):
    def build(self):
        return CalculatorLayout()


if __name__ == "__main__":
    KalkulatorApp().run()
