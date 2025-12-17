import arcade

from client.game.game_character import Character
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT


class BasicGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.mouse_x = 0
        self.mouse_y = 0

        self.player = Character(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_list.append(self.player)

        self.second_player = Character(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 200)
        self.player_list.append(self.second_player)

        wall_texture = arcade.load_texture("./textures/box.png")
        for x in range(0, SCREEN_WIDTH, 128):
            wall = arcade.Sprite()
            wall.texture = wall_texture
            wall.center_x = x
            wall.center_y = 100
            self.wall_list.append(wall)

        self.keys_pressed = set()
        self.set_fullscreen(True)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        self.player.draw_recovery()

        if self.second_player.is_dead:
            arcade.draw_circle_filled(
                self.second_player.center_x,
                self.second_player.center_y,
                50,
                arcade.color.RED
            )

    def on_update(self, delta_time: float):
        self.player.update(delta_time, self.keys_pressed, [self.mouse_x, self.mouse_y])
        self.bullet_list.update()
        self.bullets_check()

        self.player_list.update_animation()

    def bullets_check(self):
        for bullet in self.bullet_list:
            collisions = arcade.check_for_collision(bullet, self.second_player)

            if collisions:
                is_kill = self.second_player.get_damage(bullet.damage)
                if is_kill:
                    self.second_player.kill()
                    self.second_player.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

    def on_key_press(self, symbol, modifiers):
        self.keys_pressed.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys_pressed.remove(symbol)

    def on_mouse_press(self, x: float, y: float, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = self.player.shoot(x, y)
            if bullet is not None:
                self.bullet_list.append(bullet)

            # Проигрываем звук выстрела
            # arcade.play_sound(self.shoot_sound)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y
        self.player.setMouse([x, y])
