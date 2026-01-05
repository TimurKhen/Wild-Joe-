import math
import random
import uuid

import arcade

from client.variables import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, is_walking=False):
        super().__init__()
        self.texture = arcade.load_texture("./textures/bullet.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = 5000
        self.damage = 25
        self.scale = 0.01
        self.hitbox_size = 10

        target_x, target_y = self.calculate_spread(is_walking, target_x, target_y)

        self.target_x = target_x
        self.target_y = target_y

        self.id = uuid.uuid4()

        self.start_x = start_x
        self.start_y = start_y
        # Рассчитываем направление
        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        # И скорость
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed
        # Если текстура ориентирована по умолчанию вправо, то поворачиваем пулю в сторону цели
        # Для другой ориентации нужно будет подправить угол
        self.angle = math.degrees(-angle)  # Поворачиваем пулю

    def calculate_spread(self, is_walking, x, y):
        if is_walking:
            x1 = x + random.uniform(-200, 200)
            y1 = y + random.uniform(-200, 200)
            return x1, y1
        else:
            return x, y

    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
                self.center_y < 0 or self.center_y > SCREEN_HEIGHT):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

    def draw(self):
        arcade.draw_circle_outline(
            self.center_x,
            self.center_y,
            self.hitbox_size,
            arcade.color.RED
        )
