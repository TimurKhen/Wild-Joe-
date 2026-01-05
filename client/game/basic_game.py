import json
import uuid

import arcade
from arcade.gui import UIManager, UIBoxLayout, UILabel

from client.game.game_character import Character
from client.network import WSClient
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT


class BasicGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_id = uuid.uuid4()
        self.ws = WSClient(f"ws://127.0.0.1:8000/ws/{self.player_id}")

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_x, self.world_y = width, height

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.mouse_x = 0
        self.mouse_y = 0

        self.player = Character(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_list.append(self.player)

        self.second_player = Character(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 200)
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

        map_name = "./map/joe_tilemap.tmx"
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

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.box_layout = UIBoxLayout()  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.manager.add(self.box_layout)  # Всё в manager

    def setup_widgets(self):
        label = UILabel(text=f"HP: {self.player.health}",
                        font_size=20,
                        text_color=arcade.color.BLACK,
                        width=300,
                        align="left",
                        x=10,
                        y=100)
        self.box_layout.add(label)

        self.reload_label = UILabel(text=f"Ready",
                                    font_size=20,
                                    text_color=arcade.color.BLACK,
                                    width=200,
                                    align="left",
                                    x=SCREEN_WIDTH - 210,
                                    y=100)
        self.box_layout.add(self.reload_label)

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        if self.tile_map is not None:
            self.borrows_list.draw()
            self.sand_list.draw()
            self.wall_list.draw()
            self.box_list.draw()
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

        for i in self.bullet_list:
            i.draw()

        self.gui_camera.use()
        self.manager.draw()

        ### UI пользователя написать тут крч

    def on_update(self, delta_time: float = 1 / 60):
        if self.game_end:
            return

        server_data = self.get_data_from_server()
        # print(server_data)
        if server_data:
            self.set_data_to_second_player([
                server_data["x"],
                server_data["y"],
                server_data["angle"],
                server_data["status"],
                server_data["is_dead"],
                server_data["health"]
            ])

        player_information = self.player.update(delta_time, self.keys_pressed, [self.mouse_x, self.mouse_y])
        if self.player.is_recovering:
            self.reload_label.text = f'Reload: {round(1 - ((self.player.current_time - self.player.last_shot_time) / self.player.shoot_cooldown), 2)}'
        else:
            self.reload_label.text = 'Ready'

        self.send_player_data_to_server(player_information, self.bullet_list)

        self.bullet_list.update()
        self.bullets_check()
        # if self.is_one_of_players_dead():
        #     print('END OF GAME SESSION')
        #     self.game_end = True

        self.player_list.update_animation()

        # self.world_camera.position = (
        #     self.player.center_x,
        #     self.player.center_y
        # )

        if self.player_physics_engine is not None:
            self.player_physics_engine.update()

    def send_player_data_to_server(self, player_info, bullets, is_bullet_go_to_player=False):
        if player_info:
            data = {
                "x": player_info[0],
                "y": player_info[1],
                "angle": player_info[2],
                "status": player_info[3],
                "is_dead": player_info[4],
                "health": player_info[6],
                'id': str(self.player_id),
                'bullets': self.get_bullets(bullets, is_bullet_go_to_player),
                'hitbox_size': player_info[5]
            }
            self.ws.outbox.append(data)
        else:
            print('No player info')

    def get_bullets(self, bullets_list, is_bullet_go_to_player):
        bullets = []
        if is_bullet_go_to_player:
            return []

        for i in bullets_list:
            bullets.append(json.dumps({
                'x': i.center_x,
                'y': i.center_y,
                'start_x': i.start_x,
                'start_y': i.start_y,
                'target_x': i.target_x,
                'target_y': i.target_y,
                'angle': i.angle,
                'damage': i.damage,
                'id': str(i.id),
                'player': str(self.player_id),
                'hitbox_size': i.hitbox_size,
                'hit': False
            }))

        return bullets

    def get_data_from_server(self):
        if self.ws.inbox:
            for i in self.ws.inbox:
                if i['id'] == str(self.player_id):
                    print(i)
                    self.player.health = i['health']
                    self.player.is_dead = i['is_dead']
                    print(self.player.health)
                    self.ws.inbox.remove(i)
                else:
                    continue

            if self.ws.inbox:
                return self.ws.inbox.pop(0)
        return None

    def is_one_of_players_dead(self):
        if self.player.is_dead or self.second_player.is_dead:
            return True
        return False

    def set_data_to_second_player(self, data):
        self.second_player.set_data(data[0], data[1], data[2], data[3], data[4], data[5])

    def bullets_check(self):
        for bullet in self.bullet_list:
            if self.second_player.is_dead:
                continue
            collisions = arcade.check_for_collision(self.second_player, bullet)
            is_touched_wall = arcade.check_for_collision_with_list(bullet, self.collisions, 2)

            if is_touched_wall:
                bullet.remove_from_sprite_lists()

            if collisions:
                player_information = self.player.get_player_data()
                self.send_player_data_to_server(player_information, self.bullet_list, True)

                is_kill = self.second_player.get_damage(bullet.damage)
                if is_kill:
                    self.second_player.kill()
                    print(self.second_player)
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

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y
