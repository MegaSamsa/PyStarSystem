import random
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

starSys = None
label = None
canvas = None

lim = 8
multiplier = 100000
SolarRadius = 696000 / multiplier

def lerp(value0, value1, t):
    return value0 + (value1 - value0) * t

class Star:
    def __init__(self, name):
        self.name = name
        self.temperature, self.star_class, self.ratio, self.radius = self.temperature_generator()
        self.color = self.color_generator()

    def temperature_generator(self):
        rnd_value = random.uniform(0, 100)
        coef = 0.0

        for star_class, data in self.star_data.items():
            coef += data["ratio"] * 100
            if rnd_value <= coef:
                temp_range = data["temperature_range"]
                temperature = random.randint(temp_range[0], temp_range[1] - 1)
                
                if isinstance(data["radius"], list):
                    rad0, rad1 = data["radius"]
                    temp0, temp1 = data["temperature_range"]
                    radius = lerp(rad0, rad1, (temperature - temp0) / (temp1 - temp0))
                else:
                    radius = data["radius"]
                
                return temperature, star_class, data["ratio"], radius
    
    star_data = {
        "O": {
            "temperature_range": [30000, 32000],
            "ratio": 0.0000003,
            "radius": 6.6
        },
        "B": {
            "temperature_range": [9700, 30000],
            "ratio": 0.0013,
            "radius": [1.8, 6.6]
        },
        "A": {
            "temperature_range": [7200, 9700],
            "ratio": 0.006,
            "radius": [1.4, 1.8]
        },
        "F": {
            "temperature_range": [5700, 7200],
            "ratio": 0.03,
            "radius": [1.1, 1.4]
        },
        "G": {
            "temperature_range": [4900, 5700],
            "ratio": 0.076,
            "radius": [0.9, 1.1]
        },
        "K": {
            "temperature_range": [3400, 4900],
            "ratio": 0.121,
            "radius": [0.7, 0.9]
        },
        "M": {
            "temperature_range": [2100, 3400],
            "ratio": 0.765,
            "radius": 0.7
        }
    }

    def color_generator(self):
        min_temp, max_temp = (2100, 32000)
        color_red = (255, 0, 0)
        color_blue = (0, 0, 255)
        color_yellow = (255, 255, 0)

        normalized_temp = (self.temperature - min_temp) / (max_temp - min_temp)

        if normalized_temp <= 0.5:
            normalized_temp *= 2
            color = (
                int(lerp(color_red[0], color_yellow[0], normalized_temp)),
                int(lerp(color_red[1], color_yellow[1], normalized_temp)),
                int(lerp(color_red[2], color_yellow[2], normalized_temp))
            )
        else:
            normalized_temp = (normalized_temp - 0.5) * 2
            color = (
                int(lerp(color_yellow[0], color_blue[0], normalized_temp)),
                int(lerp(color_yellow[1], color_blue[1], normalized_temp)),
                int(lerp(color_yellow[2], color_blue[2], normalized_temp))
            )

        color_hex = '#%02x%02x%02x' % color
        return color_hex

class StarSystem:
    def __init__(self, name):
        self.star = Star(name)

        numList = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        num = random.choice(numList)
        self.name = str(name) + " " + num

def name_generator():
    vowels = ["a", "e", "i", "o", "u", "y"]
    consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
    name_chars = []
    
    vowel_count = random.randint(1, 2)
    consonant_count = random.randint(3, 4)

    last_char_type = ""
    same_char_count = 0

    for i in range(vowel_count + consonant_count):
        char = ""
        if last_char_type == "vowel" and same_char_count < 1:
            char = random.choice(vowels)
            same_char_count += 1
        elif last_char_type == "consonant" and same_char_count < 2:
            char = random.choice(consonants)
            same_char_count += 1
        else:
            if last_char_type == "vowel":
                char = random.choice(consonants)
                last_char_type = "consonant"
            else:
                char = random.choice(vowels)
                last_char_type = "vowel"
            same_char_count = 1

        name_chars.append(char)

    name = "".join(name_chars)
    name = name.capitalize()
    return name

def btn_exit(window):
    window.destroy()

def btn_help():
    messagebox.showinfo("Справка", "Тут будет текст.")

def visual_generator(star_name, star_radius, star_color):
    global canvas
    if canvas is not None:
        plt.close(canvas.figure)
        canvas.get_tk_widget().destroy()
    star_position = (0, 0)

    fig, ax = plt.subplots()
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal', adjustable='box')
    ax.set_axisbelow(True)
    ax.grid(True)

    star_circle = Circle(star_position, star_radius, color=star_color, fill=True)
    ax.add_patch(star_circle)
    ax.text(star_position[0], star_position[1] + star_radius + 0.25, star_name, fontsize=8, ha='center')

    canvas = FigureCanvasTkAgg(fig)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, anchor='sw')

def sys_generator():
    global starSys, label
    if label is not None:
        label.destroy()

    starSys = StarSystem(name_generator())
    star_name = starSys.star.name
    star_temperature = starSys.star.temperature
    star_class = starSys.star.star_class
    star_ratio = starSys.star.ratio
    star_radius = starSys.star.radius
    star_color = starSys.star.color

    text = (
        f"Информация о системе {starSys.name}"
        f"\nЗвезда: {star_name}"
        f"\nКласс: {star_class}"
        f"\nТемпература поверхности: {star_temperature}℃"
        f"\nДоля от звёзд: {star_ratio}"
        f"\nСолнечных радиусов: {star_radius:.3f}"
        f"\nЦвет: {star_color}"
    )
        
    visual_generator(star_name, star_radius, star_color)

    label = ttk.Label(text=text, justify=tk.LEFT, background='white')
    label.place(relx=0.0, rely=1.0, anchor='sw')
    
def main():
    global window
    window = Tk()
    window.title("StarSys")
    window.geometry("640x480")
    window.iconbitmap("sun.ico")

    menu = Menu()
    options = Menu(tearoff=0)
    menu.add_cascade(label="Файл", menu=options)
    options.add_command(label="Сгенерировать систему", command=sys_generator)
    options.add_command(label="Сохранить систему")
    options.add_separator()
    options.add_command(label="Выйти", command=lambda:btn_exit(window))
    menu.add_cascade(label="Вид")
    menu.add_cascade(label="Справка", command=btn_help)
    window.config(menu=menu)

    sys_generator()

    window.mainloop()

main()