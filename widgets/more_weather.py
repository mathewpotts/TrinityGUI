import tkinter as tk
import os
from PIL import ImageTk, Image

class MoreWeatherWidget:
    def __init__(self,root):
        self.popup = tk.Toplevel(root)
        self.popup.title("More Weather")

        global wind_dir_dt
        wind_dir_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Wind_direction_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.wind_dir_dt_label = tk.Label(self.popup, image = wind_dir_dt)
        self.wind_dir_dt_label.grid(row = 0, column = 0)

        global wind_v_dt
        wind_v_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Wind_speed_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.wind_v_dt_label = tk.Label(self.popup, image = wind_v_dt)
        self.wind_v_dt_label.grid(row = 0, column = 1)

        global temp_dt
        temp_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Temperature_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.temp_dt_label = tk.Label(self.popup, image = temp_dt)
        self.temp_dt_label.grid(row = 1, column = 0)

        global pressure_dt
        pressure_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Pressure_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.pressure_dt_label = tk.Label(self.popup, image = pressure_dt)
        self.pressure_dt_label.grid(row = 1, column = 1)

        global hum_dt
        hum_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Humidity_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.hum_dt_label = tk.Label(self.popup, image = hum_dt)
        self.hum_dt_label.grid(row = 2, column = 0)

        global dp_dt
        dp_dt = ImageTk.PhotoImage(Image.open(f"{os.environ['WPDIR']}/Dewpoint_over_time.png").resize((350, 350))) # get the image import into tkinter
        self.dp_dt_label = tk.Label(self.popup, image = dp_dt)
        self.dp_dt_label.grid(row = 2, column = 1)

        close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy)
        close_button.grid(row = 1, column = 1)
