import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def zapusk_snaryada():     #запуск анимации снаряда
    global animatsiya, vremya
    vremya = 0
    nachalnaya_skorost = float(skorost_spinbox.get())
    ugol = float(ugol_slider.get())
    massa = float(massa_spinbox.get())

    ugol_v_radianah = np.radians(ugol)
#для координат
    def koordinata_x(vremya):
        return nachalnaya_skorost * np.cos(ugol_v_radianah) * vremya

    def koordinata_y(vremya):
        return nachalnaya_skorost * np.sin(ugol_v_radianah) * vremya - 0.5 * gravitatsiya * vremya**2

    def obnovlenie(kadr):
        global vremya
        vremya += shag_vremeni
        pozitsiya_x = koordinata_x(vremya)
        pozitsiya_y = koordinata_y(vremya)

        if pozitsiya_y <= 0:  #стоп анимации если он уже на земле
            animatsiya.event_source.stop()
            return snaryad.set_data([], [])

        snaryad.set_data([pozitsiya_x], [pozitsiya_y])
        return snaryad,

    #очистить график перед новой
    os.clear()
    os.set_xlim(0, 2 * (nachalnaya_skorost**2) * np.sin(2 * ugol_v_radianah) / gravitatsiya)  # Maksimalnaya dalnost poleta
    os.set_ylim(0, (nachalnaya_skorost**2) * (np.sin(ugol_v_radianah)**2) / (2 * gravitatsiya))  # Maksimalnaya vysota
    os.set_xlabel("Gorizontalnoe rasstoyanie (m)")
    os.set_ylabel("Vysota (m)")
    os.grid()

    snaryad, = os.plot([], [], 'ro')

    animatsiya = FuncAnimation(figura, obnovlenie, frames=np.arange(0, 1000), interval=shag_vremeni * 1000, blit=True)
    holst.draw()

def sbros():
    global vremya     #сброс параметров графика
    vremya = 0
    skorost_spinbox.delete(0, tk.END)
    skorost_spinbox.insert(0, "20")
    ugol_slider.set(45)
    massa_spinbox.delete(0, tk.END)
    massa_spinbox.insert(0, "1")

    os.clear()
    os.set_xlim(0, 10)
    os.set_ylim(0, 10)
    os.set_xlabel("Горизонтальное расстояние (m)")
    os.set_ylabel("Высота(m)")
    os.grid()
    holst.draw()

gravitatsiya = 9.81
shag_vremeni = 0.05
#создание окна
okno = tk.Tk()
okno.title("Симуляция снаряда")

panel_upravleniya = ttk.Frame(okno)
panel_upravleniya.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

skorost_label = ttk.Label(panel_upravleniya, text="Начальная скорость (m/s):")
skorost_label.pack()
skorost_spinbox = ttk.Spinbox(panel_upravleniya, from_=1, to=100, increment=1)
skorost_spinbox.pack()
skorost_spinbox.insert(0, "20")

ugol_label = ttk.Label(panel_upravleniya, text="Угол запуска:")
ugol_label.pack()
ugol_slider = ttk.Scale(panel_upravleniya, from_=0, to=90, orient="horizontal")
ugol_slider.pack()
ugol_slider.set(45)

massa_label = ttk.Label(panel_upravleniya, text="Масса (kg):")
massa_label.pack()
massa_spinbox = ttk.Spinbox(panel_upravleniya, from_=0.1, to=10, increment=0.1)
massa_spinbox.pack()
massa_spinbox.insert(0, "1")

zapusk_knopka = ttk.Button(panel_upravleniya, text="Запуск", command=zapusk_snaryada)
zapusk_knopka.pack(pady=5)
sbros_knopka = ttk.Button(panel_upravleniya, text="Сброс", command=sbros)
sbros_knopka.pack(pady=5)

#график
figura, os = plt.subplots()
holst = FigureCanvasTkAgg(figura, master=okno)
holst.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

sbros()
#запуск цикла
okno.mainloop()
