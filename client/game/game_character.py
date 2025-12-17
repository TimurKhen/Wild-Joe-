import math

import arcade

from client.game.bullet_object import Bullet
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT


class Character(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 1.0
        self.speed = 300
        self.health = 100

        self.idle_texture = arcade.load_texture('./textures/character_idle.png')
        self.texture = self.idle_texture

        # self.current_texture = 0
        # self.texture_change_time = 0
        # self.texture_change_delay = 0.1  # секунд на кадр

        # self.walk_textures = []
        # for i in range(0, 8):
        #     texture = arcade.load_texture(f":resources:/images/animated_characters/male_person/malePerson_walk{i}.png")
        #     self.walk_textures.append(texture)

        self.bullet_speed = 500
        self.fire_rate = 1
        self.shoot_cooldown = 1.0 / self.fire_rate
        self.last_shot_time = 0.0
        self.can_shoot = True

        self.is_walking = False
        self.direction_angle = 0
        self.object_size = 40

        self.angle = 0

        self.ammo = 8
        self.is_shot = False
        self.current_time = 0

        self.recovery_indicator_visible = False
        self.recovery_progress = 0.0  # от 0 до 1
        self.indicator_pulse = 0.0
        self.indicator_pulse_speed = 3.0
        self.is_recovering = False
        self.is_dead = False

    def setMouse(self, mouse_x_y):
        mouse_x, mouse_y = mouse_x_y

        # Вычисляем угол между персонажем и курсором мыши
        dx = mouse_x - self.center_x
        dy = mouse_y - self.center_y

        # Устанавливаем угол поворота персонажа
        # atan2 возвращает угол в радианах, преобразуем в градусы
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        self.angle = -angle_deg

    def update(self, delta_time, keys_pressed, mouse_x_y):
        if self.is_dead:
            return
        self.setMouse(mouse_x_y)

        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        if self.center_x + dx + self.object_size >= SCREEN_WIDTH or self.center_x + dx - self.object_size <= 0:
            dx = 0

        if self.center_y + dy + self.object_size >= SCREEN_HEIGHT or self.center_y + dy - self.object_size <= 0:
            dy = 0

        self.center_x += dx
        self.center_y += dy

        self.is_walking = dx or dy
        self.current_time += delta_time

        return [self.center_x, self.center_y, self.angle, self.is_walking, self.is_dead]

    def shoot(self, x, y):
        if self.is_dead:
            return None

        current_time = self.current_time
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            start_x = self.center_x
            start_y = self.center_y
            target_x = x
            target_y = y

            bullet = Bullet(
                start_x, start_y,
                target_x, target_y,
                self.bullet_speed
            )

            self.last_shot_time = current_time

            return bullet
        else:
            return None

    def draw_recovery(self):
        if self.is_dead:
            return None

        if self.current_time - self.last_shot_time >= self.shoot_cooldown:
            self.is_recovering = False
        else:
            self.is_recovering = True

        if not self.is_recovering:
            return

        indicator_x = self.center_x
        indicator_y = self.center_y

        arcade.draw_arc_outline(
            indicator_x, indicator_y,
            150, 150, arcade.color.RED,
            360 - (self.current_time - self.last_shot_time) / self.shoot_cooldown * 360, 360, 3
        )

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            return True
        return False

    # def update_animation(self, delta_time: float = 1 / 60):
    #     """ Обновление анимации """
    #     if self.is_walking:
    #         self.texture_change_time += delta_time
    #         if self.texture_change_time >= self.texture_change_delay:
    #             self.texture_change_time = 0
    #             self.current_texture += 1
    #             if self.current_texture >= len(self.walk_textures):
    #                 self.current_texture = 0

    def set_data(self, new_x, new_y, new_angle, new_is_walking, new_is_dead):
        self.center_x = new_x
        self.center_y = new_y
        self.angle = new_angle
        self.is_walking = new_is_walking
        self.is_dead = new_is_dead
