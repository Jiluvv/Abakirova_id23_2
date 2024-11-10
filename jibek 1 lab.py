import tkinter as tk
import math

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas_size = 600
        self.radius = 200
        self.angle = 0  # Начальный угол
        self.speed = 2  # Скорость движения точки
        self.direction = 1  # 1 - по часовой стрелке, -1 - против часовой стрелки

        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        # Рисуем круг
        self.draw_circle()

        # Запускаем анимацию
        self.update_position()

    def draw_circle(self):
        x_center = self.canvas_size // 2
        y_center = self.canvas_size // 2
        self.canvas.create_oval(
            x_center - self.radius, y_center - self.radius,
            x_center + self.radius, y_center + self.radius,
            outline='black', fill='', width=2
        )

    def update_position(self):
        # Вычисляем координаты точки
        x_center = self.canvas_size // 2
        y_center = self.canvas_size // 2

        x = x_center + self.radius * math.cos(math.radians(self.angle))
        y = y_center + self.radius * math.sin(math.radians(self.angle))

        # Рисуем точку
        self.canvas.delete('point')  # Удаляем предыдущую точку
        self.canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5,
            outline='purple', fill='purple', tags='point'
        )

        # Обновляем угол
        self.angle += self.speed * self.direction
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        # Повторяем обновление позиции
        self.master.after(50, self.update_position)  # Обновляем каждые 50 мс

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Moving Point on Circle")
    app = DrawingApp(root)
    root.mainloop()