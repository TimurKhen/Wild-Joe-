import arcade
from arcade.gui import UIManager, UIBoxLayout, UILabel, UIAnchorLayout

from client.game.game_character import Character
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT


class BasicGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_x, self.world_y = width, height

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.mouse_x = 0
        self.mouse_y = 0

        self.player = Character(200, SCREEN_HEIGHT / 2)
        self.player_list.append(self.player)

        self.second_player = Character(SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2 - 200, True)
        self.player_list.append(self.second_player)

        self.keys_pressed = set()
        # self.set_fullscreen(True)
        self.game_end = False

        self.collisions = arcade.SpriteList()

        self.tile_map = None
        self.player_physics_engine = None
        self.wall_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()
        self.borrows_list = arcade.SpriteList()
        self.sand_list = arcade.SpriteList()

        self.set_map()

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.box_layout = UIBoxLayout()  # Вертикальный стек
        self.box_layout_2 = UIBoxLayout(x=SCREEN_WIDTH - 300)

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.manager.add(self.box_layout)  # Всё в manager
        self.manager.add(self.box_layout_2)  # Всё в manager

    def set_map(self, map_name="joe"):
        map_name = f"./map/{map_name}_tilemap.tmx"
        layer_options = {
            'borrows': {
                'use_spatial_hash': True
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, 1, layer_options)

        self.collisions = self.tile_map.sprite_lists['collisions']
        # self.collisions.append(self.second_player)

        self.player_physics_engine = arcade.PhysicsEngineSimple(self.player, self.collisions)

        self.wall_list = self.tile_map.sprite_lists['walls']
        self.borrows_list = self.tile_map.sprite_lists['borrows']
        self.sand_list = self.tile_map.sprite_lists['sand']
        self.box_list = self.tile_map.sprite_lists['box']

    def setup_widgets(self):
        self.player_health = UILabel(text=f"HP: {self.player.health}",
                                     font_size=20,
                                     text_color=arcade.color.BLACK,
                                     width=300,
                                     align="left",
                                     x=10,
                                     y=100)
        self.box_layout.add(self.player_health)

        self.reload_label = UILabel(text=f"Ready",
                                    font_size=20,
                                    text_color=arcade.color.BLACK,
                                    width=200,
                                    align="left",
                                    x=SCREEN_WIDTH - 210,
                                    y=100)
        self.box_layout.add(self.reload_label)

        self.player_2_health = UILabel(text=f"HP: {self.second_player.health}",
                                       font_size=20,
                                       text_color=arcade.color.BLACK,
                                       width=300,
                                       align="left",
                                       x=SCREEN_WIDTH - 100,
                                       y=100)
        self.box_layout_2.add(self.player_2_health)

        self.reload_player_2_label = UILabel(text=f"Ready",
                                             font_size=20,
                                             text_color=arcade.color.BLACK,
                                             width=200,
                                             align="left",
                                             x=SCREEN_WIDTH - 210,
                                             y=100)
        self.box_layout_2.add(self.reload_label)

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        if self.tile_map is not None:
            self.sand_list.draw()
            self.wall_list.draw()
            self.box_list.draw()
            # self.borrows_list.draw()
        # self.scene.draw()

        self.bullet_list.draw()
        self.player_list.draw()
        for i in self.player_list:
            i.draw()

        if self.second_player.is_dead:
            arcade.draw_circle_filled(
                self.second_player.center_x,
                self.second_player.center_y,
                50,
                arcade.color.RED
            )

        if self.player.is_dead:
            arcade.draw_circle_filled(
                self.player.center_x,
                self.player.center_y,
                50,
                arcade.color.RED
            )

        for i in self.bullet_list:
            i.draw()

        self.gui_camera.use()
        self.manager.draw()

        ### UI пользователя написать тут крч

    def on_update(self, delta_time: float = 1 / 60):
        if self.game_end:
            return

        self.player.update(delta_time, self.keys_pressed)
        self.second_player.update(delta_time, self.keys_pressed)

        if self.player.is_recovering:
            self.reload_label.text = f'Reload: {round(1 - ((self.player.current_time - self.player.last_shot_time) / self.player.shoot_cooldown), 2)}'
        else:
            self.reload_label.text = 'Ready'

        if self.second_player.is_recovering:
            self.reload_player_2_label.text = f'Reload: {round(1 - ((self.second_player.current_time - self.second_player.last_shot_time) / self.second_player.shoot_cooldown), 2)}'
        else:
            self.reload_player_2_label.text = 'Ready'

        self.bullet_list.update()
        self.bullets_check()

        self.player_list.update_animation()

        if self.player_physics_engine is not None:
            self.player_physics_engine.update()

        self.player_health.text = f'HP: {self.player.health}'
        self.player_2_health.text = f'HP: {self.second_player.health}'

    def check_winner(self):
        if self.player.is_dead:
            self.game_end = True
            self.make_winner_screen(-1)
            lose_sound = arcade.load_sound('./sounds/lostround (1).mp3')
            arcade.play_sound(lose_sound)
            # TODO
            #  Экран конца победа врага
        elif self.second_player.is_dead:
            self.game_end = True
            self.make_winner_screen(1)
            win_sound = arcade.load_sound('./sounds/wonround.mp3')
            arcade.play_sound(win_sound)
            # TODO
            #  Экран конца победа игрока
        else:
            return

    def make_winner_screen(self, winner):
        status = ''
        if winner == 1:
            status = 'Выйграл игрок 1'
        elif winner == -1:
            status = 'Выйграл игрок 2'

        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout_2 = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        self.anchor_layout.add(self.box_layout_2)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

        label = UILabel(text=f"{status}",
                        font_size=20,
                        text_color=arcade.color.BLACK,
                        width=300,
                        align="center",
                        x=10,
                        y=100)
        self.box_layout_2.add(label)

    def is_one_of_players_dead(self):
        if self.player.is_dead or self.second_player.is_dead:
            return True
        return False

    def bullets_check(self):
        for bullet in self.bullet_list:
            if self.second_player.is_dead:
                continue
            collisions_first = arcade.check_for_collision(self.player, bullet)
            collisions_second = arcade.check_for_collision(self.second_player, bullet)
            is_touched_wall = arcade.check_for_collision_with_list(bullet, self.collisions)

            if is_touched_wall:
                bullet.remove_from_sprite_lists()

            if collisions_second:
                is_kill = self.second_player.get_damage(bullet.damage)
                if is_kill:
                    self.second_player.kill()
                    print(self.second_player)
                    self.second_player.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

            if collisions_first:
                is_kill = self.player.get_damage(bullet.damage)
                if is_kill:
                    self.player.kill()
                    print(self.player)
                    self.player.remove_from_sprite_lists()
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

        ### Заменить на пробел!!!!!!

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y

        ### Заменить на q e и del + pg down

##### ЛОКАЛЬНЫЙ КООП + ПОВОРОТ НА QE
