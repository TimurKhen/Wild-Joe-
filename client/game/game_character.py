import math

import arcade

from client.game.bullet_object import Bullet
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT, SHOW_HITBOX


class Character(arcade.Sprite):
    def __init__(self, x, y, is_second=False):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = 150
        self.health = 100
        self.is_second = is_second

        self.idle_texture = arcade.load_texture('./textures/player_idle.png')
        self.scale = 0.3
        self.texture = self.idle_texture

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1

        self.walk_textures = []
        for i in range(1, 3):
            texture = arcade.load_texture(f"./textures/player_walk_{i}.png")
            self.walk_textures.append(texture)

        self.bullet_speed = 500
        self.fire_rate = 1
        self.shoot_cooldown = 1.0 / self.fire_rate
        self.last_shot_time = 0.0
        self.can_shoot = True

        self.is_walking = False
        self.hitbox_size = 60

        # Угол поворота персонажа (в градусах)
        self.angle = 0

        self.ammo = 8
        self.is_shot = False
        self.current_time = 0

        self.recovery_indicator_visible = False
        self.recovery_progress = 0.0
        self.indicator_pulse = 0.0
        self.indicator_pulse_speed = 3.0
        self.is_recovering = False
        self.is_dead = False

        self.shoot_sound = arcade.load_sound('./sounds/deagle-1.mp3')
        self.reload_sound = arcade.load_sound('./sounds/reload.mp3')

        self.gun_length = 50

    def update(self, delta_time, keys_pressed):
        if self.is_dead:
            return

        dx, dy = 0, 0

        if not self.is_second:
            if arcade.key.A in keys_pressed:
                dx -= self.speed * delta_time
            if arcade.key.D in keys_pressed:
                dx += self.speed * delta_time
            if arcade.key.W in keys_pressed:
                dy += self.speed * delta_time
            if arcade.key.S in keys_pressed:
                dy -= self.speed * delta_time
        else:
            if arcade.key.LEFT in keys_pressed:
                dx -= self.speed * delta_time
            if arcade.key.RIGHT in keys_pressed:
                dx += self.speed * delta_time
            if arcade.key.UP in keys_pressed:
                dy += self.speed * delta_time
            if arcade.key.DOWN in keys_pressed:
                dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        if self.center_x + dx + self.hitbox_size >= SCREEN_WIDTH or self.center_x + dx - self.hitbox_size <= 0:
            dx = 0

        if self.center_y + dy + self.hitbox_size >= SCREEN_HEIGHT or self.center_y + dy - self.hitbox_size <= 0:
            dy = 0

        self.center_x += dx
        self.center_y += dy

        self.is_walking = dx != 0 or dy != 0
        self.current_time += delta_time

    def get_player_data(self):
        return [self.center_x, self.center_y, self.angle, self.is_walking, self.is_dead, self.hitbox_size, self.health]

    def shoot(self):
        if self.is_dead:
            return None

        current_time = self.current_time
        if current_time - self.last_shot_time < self.shoot_cooldown:
            return None

        rad = math.radians(self.angle)

        dir_x = math.cos(rad)
        dir_y = -math.sin(rad)  # ← ВАЖНО

        muzzle_offset = self.width * 0.5

        start_x = self.center_x + dir_x * muzzle_offset
        start_y = self.center_y + dir_y * muzzle_offset

        target_distance = 1000
        target_x = start_x + dir_x * target_distance
        target_y = start_y + dir_y * target_distance

        bullet = Bullet(
            start_x,
            start_y,
            target_x,
            target_y,
            self.is_walking
        )

        self.last_shot_time = current_time

        arcade.play_sound(self.shoot_sound, volume=0.3)
        arcade.play_sound(self.reload_sound)

        return bullet

    def draw_recovery(self):
        if self.is_dead:
            return None

        if self.current_time - self.last_shot_time >= self.shoot_cooldown:
            self.is_recovering = False
        else:
            self.is_recovering = True

        if not self.is_recovering:
            return

    def draw_object_hit_box(self):
        if self.is_dead:
            return None

        arcade.draw_circle_outline(
            self.center_x, self.center_y,
            self.hitbox_size, color=arcade.color.RED,
        )

    def draw(self):
        self.draw_recovery()

        if SHOW_HITBOX:
            self.draw_object_hit_box()

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            return True
        return False

    def set_health(self, new_health):
        self.health = new_health

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                self.texture = self.walk_textures[self.current_texture]
        else:
            self.texture = self.idle_texture
            self.current_texture = 0
            self.texture_change_time = 0

    def set_data(self, new_x, new_y, new_angle, new_status, new_is_dead, new_health):
        self.center_x = new_x
        self.center_y = new_y
        self.angle = new_angle
        self.is_walking = new_status
        self.is_dead = new_is_dead
        self.health = new_health
