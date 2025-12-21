import math
import uuid

import arcade

from client.variables import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, speed=100000, damage=50):
        super().__init__()
        self.texture = arcade.load_texture("./textures/bullet.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage
        self.scale = 0.02
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
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        # Если текстура ориентирована по умолчанию вправо, то поворачиваем пулю в сторону цели
        # Для другой ориентации нужно будет подправить угол
        self.angle = math.degrees(-angle)  # Поворачиваем пулю

    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
                self.center_y < 0 or self.center_y > SCREEN_HEIGHT):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
