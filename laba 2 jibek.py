import pygame
import math
import json

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Волны и поплавки")

background_color = (240, 240, 240)
wave_color = (128, 0, 0)
poplavok_color = (0, 0, 90)

with open("volny.json") as file:
    data = json.load(file)

num_waves = data["number of waves"]
wave_params = data["waves"]
poplavok_params = data["poplavki"]
poplavok_radius = data["poplavok radius"]
poplavok_positions = [height // (num_waves + 1) * (i + 1) for i in range(num_waves)]

g = 9.81
offset_scale = 5

def calculate_wave_y(wave_y, amplitude, period, speed, time, x):
    return wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * time)

def calculate_offset(mass, objem):
    return ((mass - objem) * g / (mass + objem)) * offset_scale

def draw_wave(wave_y, amplitude, period, speed, time):
    for x in range(width):
        y = calculate_wave_y(wave_y, amplitude, period, speed, time, x)
        pygame.draw.circle(window, wave_color, (x, int(y)), 1)

def draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem):
    wave_height = calculate_wave_y(wave_y, amplitude, period, speed, time, poplavok_x)
    offset = calculate_offset(mass, objem)
    poplavok_y = wave_height + offset
    pygame.draw.circle(window, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)

def main_loop():
    running = True
    clock = pygame.time.Clock()

    while running:
        window.fill(background_color)
        time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i, wave in enumerate(wave_params):
            amplitude, period, speed = wave["amplitude"], wave["period"], wave["speed"]
            mass, objem = poplavok_params[i]["mass"], poplavok_params[i]["objem"]
            wave_y = poplavok_positions[i]  # вертикальная позиция волны

            draw_wave(wave_y, amplitude, period, speed, time)  # рисуем волну
            poplavok_x = (time * 100) % width  # движение поплавка по оси X
            draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem)  # рисуем поплавок

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
main_loop()

def draw_wave(wave_y, amplitude, period, speed, time):
    for x in range(width):
        y = calculate_wave_y(wave_y, amplitude, period, speed, time, x)
        pygame.draw.circle(window, wave_color, (x, int(y)), 1)

def draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem):
    wave_height = calculate_wave_y(wave_y, amplitude, period, speed, time, poplavok_x)
    offset = calculate_offset(mass, objem)
    poplavok_y = wave_height + offset
    pygame.draw.circle(window, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)

def main_loop():
    running = True
    clock = pygame.time.Clock()

    while running:
        window.fill(background_color)
        time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i, wave in enumerate(wave_params):
            amplitude, period, speed = wave["amplitude"], wave["period"], wave["speed"]
            mass, objem = poplavok_params[i]["mass"], poplavok_params[i]["objem"]
            wave_y = poplavok_positions[i]  # вертикальная позиция волны

            draw_wave(wave_y, amplitude, period, speed, time)  # рисуем волну
            poplavok_x = (time * 100) % width  # движение поплавка по оси X
            draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem)  # рисуем поплавок

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
main_loop()