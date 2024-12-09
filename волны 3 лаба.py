import pygame
import math
import json
import os
import tkinter as tk
from tkinter import Toplevel, Label, Spinbox, Button

pygame.init()

shirina, visota = 800, 600
okno = pygame.display.set_mode((shirina, visota))
pygame.display.set_caption("Волны и поплавки")

cvet_fona = (240, 240, 240)
cvet_volny = (0, 100, 255)
cvet_poplavka = (255, 0, 0)

imja_fajla = "volny_data.json"

default_data = {
    "волны": [
        {"амплитуда": 30, "период": 150, "скорость": 1.2},
        {"амплитуда": 40, "период": 120, "скорость": 1.5},
    ],
    "поплавки": [
        {"масса": 50, "объем": 50},
        {"масса": 60, "объем": 70},
    ],
    "радиус поплавка": 15
}

if not os.path.exists(imja_fajla):
    with open(imja_fajla, "w") as file:
        json.dump(default_data, file, ensure_ascii=False, indent=4)

try:
    with open(imja_fajla, "r") as file:
        data = json.load(file)
        if "волны" not in data or not isinstance(data["волны"], list):
            print("Ключ 'волны' отсутствует или поврежден. Использую значения по умолчанию.")
            data = default_data
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Ошибка при загрузке данных: {e}. Использую значения по умолчанию.")
    data = default_data

volny = data["волны"]
poplavki = data["поплавки"]
radiys_poplavka = data["радиус поплавка"]

def obnovit_pozicii():
    global pozicii_poplavkov
    pozicii_poplavkov = [visota // (len(volny) + 1) * (i + 1) for i in range(len(volny))]

obnovit_pozicii()

pausa = False
rabota = True
vremja = 0
vremja_nachala = 0
vremja_pauzi = 0

aktivnye_tk_okna = []

def dobavit_volnu():
    volny.append({"амплитуда": 30, "период": 150, "скорость": 1.0})
    poplavki.append({"масса": 50, "объем": 50})
    obnovit_pozicii()

def udalit_volnu():
    if volny:
        volny.pop()
        poplavki.pop()
        obnovit_pozicii()

import threading

def otkryt_nastroyki(index, yvo_volna):
    def potokovaya_funkciya():
        def obnovit_znacheniya():
            try:
                if yvo_volna:
                    volny[index]["амплитуда"] = int(amplitude_spinbox.get())
                    volny[index]["период"] = int(period_spinbox.get())
                    volny[index]["скорость"] = float(speed_spinbox.get())
                else:
                    poplavki[index]["масса"] = float(mass_spinbox.get())
                    poplavki[index]["объем"] = float(volume_spinbox.get())
                nastroyka_okno.destroy()
            except ValueError:
                print("Ошибка: некорректные значения")

        root = tk.Tk()
        root.withdraw()
        nastroyka_okno = Toplevel(root)
        nastroyka_okno.title("Настройка параметров")

        if yvo_volna:
            Label(nastroyka_okno, text="Амплитуда:").pack()
            amplitude_spinbox = Spinbox(nastroyka_okno, from_=1, to=100, increment=1)
            amplitude_spinbox.delete(0, "end")
            amplitude_spinbox.insert(0, volny[index]["амплитуда"])
            amplitude_spinbox.pack()

            Label(nastroyka_okno, text="Период:").pack()
            period_spinbox = Spinbox(nastroyka_okno, from_=10, to=300, increment=10)
            period_spinbox.delete(0, "end")
            period_spinbox.insert(0, volny[index]["период"])
            period_spinbox.pack()

            Label(nastroyka_okno, text="Скорость:").pack()
            speed_spinbox = Spinbox(nastroyka_okno, from_=0.1, to=10.0, increment=0.1, format="%.1f")
            speed_spinbox.delete(0, "end")
            speed_spinbox.insert(0, volny[index]["скорость"])
            speed_spinbox.pack()
        else:
            Label(nastroyka_okno, text="Масса:").pack()
            mass_spinbox = Spinbox(nastroyka_okno, from_=1, to=100, increment=1)
            mass_spinbox.delete(0, "end")
            mass_spinbox.insert(0, poplavki[index]["масса"])
            mass_spinbox.pack()

            Label(nastroyka_okno, text="Объем:").pack()
            volume_spinbox = Spinbox(nastroyka_okno, from_=1, to=100, increment=1)
            volume_spinbox.delete(0, "end")
            volume_spinbox.insert(0, poplavki[index]["объем"])
            volume_spinbox.pack()

        Button(nastroyka_okno, text="Сохранить", command=obnovit_znacheniya).pack()

        root.mainloop()

    potok = threading.Thread(target=potokovaya_funkciya)
    potok.start()

def narisovat_volnu(volna_y, amplituda, period, skorost):
    for x in range(shirina):
        y = volna_y + amplituda * math.sin(2 * math.pi * (x / period) - skorost * vremja)
        pygame.draw.circle(okno, cvet_volny, (x, int(y)), 1)

def narisovat_poplavok(volna_y, amplituda, period, skorost, poplavok_x, massa, objem):
    vysota_volny = volna_y + amplituda * math.sin(2 * math.pi * (poplavok_x / period) - skorost * vremja)
    smeshchenie = ((objem - massa) * 9.81 / max(1, massa + objem)) * 5  # Архимедова сила
    poplavok_y = vysota_volny + smeshchenie
    pygame.draw.circle(okno, cvet_poplavka, (int(poplavok_x), int(poplavok_y)), radiys_poplavka)

def obrabotka_klika(myshi_x, myshi_y):
    for i, volna_y in enumerate(pozicii_poplavkov):
        poplavok_x = (vremja * 100) % shirina
        vysota_volny = volna_y + volny[i]["амплитуда"] * math.sin(2 * math.pi * (poplavok_x / volny[i]["период"]) - volny[i]["скорость"] * vremja)
        smeshchenie = ((poplavki[i]["объем"] - poplavki[i]["масса"]) * 9.81 / max(1, poplavki[i]["масса"] + poplavki[i]["объем"])) * 5
        poplavok_y = vysota_volny + smeshchenie

        if (myshi_x - poplavok_x) ** 2 + (myshi_y - poplavok_y) ** 2 <= radiys_poplavka ** 2:
            otkryt_nastroyki(i, False)
            return
        elif abs(myshi_y - volna_y) < 10:
            otkryt_nastroyki(i, True)
            return

chasy = pygame.time.Clock()

while rabota:
    okno.fill(cvet_fona)

    for tk_okno in aktivnye_tk_okna:
        tk_okno.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rabota = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pausa = not pausa
                if pausa:
                    vremja_pauzi = pygame.time.get_ticks() / 1000 - vremja_nachala
                else:
                    vremja_nachala = pygame.time.get_ticks() / 1000 - vremja_pauzi
            elif event.key == pygame.K_a:
                dobavit_volnu()
            elif event.key == pygame.K_d:
                udalit_volnu()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            obrabotka_klika(*event.pos)

    if not pausa:
        vremja = pygame.time.get_ticks() / 1000 - vremja_nachala
        for i, volna in enumerate(volny):
            narisovat_volnu(pozicii_poplavkov[i], volna["амплитуда"], volna["период"], volna["скорость"])
            narisovat_poplavok(pozicii_poplavkov[i], volna["амплитуда"], volna["период"], volna["скорость"], (vremja * 100) % shirina, poplavki[i]["масса"], poplavki[i]["объем"])

    pygame.display.update()
    chasy.tick(60)

with open(imja_fajla, "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

pygame.quit()
