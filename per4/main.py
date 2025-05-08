import tkinter as tk
from tkinter import ttk
import random
import datetime
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import serial
import serial.tools.list_ports


class FireDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fire Detection System")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.sensor_value = tk.IntVar(value=0)
        self.fire_status = tk.StringVar(value="AMAN")
        self.fan_status = tk.StringVar(value="MATI")
        self.fan_manual_off = False

        self.history = deque(maxlen=30)

        self.setup_ui()
        self.setup_plot()
        self.connect_serial()  # Panggil ini dulu!
        self.update_sensor()

    def setup_ui(self):
        ttk.Label(self.root, text="🔥 Fire Detection System",
                  font=("Helvetica", 16)).pack(pady=10)

        frame_info = ttk.Frame(self.root)
        frame_info.pack(pady=5)

        ttk.Label(frame_info, text="Sensor MQ-2 Value:").grid(row=0,
                                                              column=0, sticky="w")
        ttk.Label(frame_info, textvariable=self.sensor_value, font=(
            "Helvetica", 12)).grid(row=0, column=1, sticky="w")

        ttk.Label(frame_info, text="Status Kebakaran:").grid(
            row=1, column=0, sticky="w")
        ttk.Label(frame_info, textvariable=self.fire_status, font=(
            "Helvetica", 12, "bold"), foreground="red").grid(row=1, column=1, sticky="w")

        ttk.Label(frame_info, text="Kipas:").grid(row=2, column=0, sticky="w")
        ttk.Label(frame_info, textvariable=self.fan_status, font=(
            "Helvetica", 12), foreground="blue").grid(row=2, column=1, sticky="w")

        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Matikan Kipas",
                   command=self.turn_off_fan).pack(side="left", padx=10)
        ttk.Button(frame_buttons, text="Keluar",
                   command=self.root.quit).pack(side="left", padx=10)

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.line, = self.ax.plot([], [], color='red')
        self.ax.set_ylim(0, 1024)
        self.ax.set_xlim(0, 30)
        self.ax.set_title("Grafik Nilai Sensor MQ-2")
        self.ax.set_ylabel("Asap (analog)")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def update_sensor(self):
        if self.serial_port and self.serial_port.in_waiting:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                value = int(line)
                self.sensor_value.set(value)

                if value > 400 and not self.fan_manual_off:
                    self.fire_status.set("BAHAYA")
                    self.fan_status.set("MENYALA")
                elif self.fan_manual_off:
                    self.fire_status.set("AMAN")
                    self.fan_status.set("DIMATIKAN MANUAL")
                else:
                    self.fire_status.set("AMAN")
                    self.fan_status.set("MATI")

                self.save_to_log(value)
                self.update_graph(value)

            except Exception as e:
                print("Gagal membaca dari serial:", e)

        self.root.after(1000, self.update_sensor)

    def update_graph(self, value):
        self.history.append(value)
        self.line.set_ydata(self.history)
        self.line.set_xdata(range(len(self.history)))
        self.ax.set_xlim(0, len(self.history))
        self.canvas.draw()

    def save_to_log(self, value):
        with open("fire_log.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [datetime.datetime.now().isoformat(), value, self.fire_status.get()])

    def turn_off_fan(self):
        self.fan_manual_off = True
        self.fan_status.set("DIMATIKAN MANUAL")

    def connect_serial(self):
        try:
            self.serial_port = serial.Serial(
                'COM3', 115200, timeout=1)  # ganti COM4 sesuai port kamu
        except serial.SerialException:
            self.serial_port = None
            print("ESP32 tidak terhubung.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FireDetectionApp(root)
    root.mainloop()
