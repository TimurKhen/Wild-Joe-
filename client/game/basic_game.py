import uuid

import arcade

from client.game.game_character import Character
from client.network import WSClient
from client.variables import SCREEN_WIDTH, SCREEN_HEIGHT


class BasicGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_id = str(uuid.uuid4())
        self.ws = WSClient(f"ws://127.0.0.1:8000/ws/{self.player_id}")

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
        # self.set_fullscreen(True)
        self.game_end = False

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

    def on_update(self, delta_time: float = 1 / 60):
        if self.game_end:
            return

        server_data = self.get_data_from_server()
        print(server_data)
        if server_data:
            self.set_data_to_second_player([
                server_data["x"],
                server_data["y"],
                server_data["angle"],
                server_data["status"],
                server_data["is_dead"],
                server_data["id"],
            ])

        player_information = self.player.update(delta_time, self.keys_pressed, [self.mouse_x, self.mouse_y])
        self.send_data_to_server(player_information)

        self.bullet_list.update()
        self.bullets_check()
        if self.is_one_of_players_dead():
            print('END OF GAME SESSION')
            self.game_end = True

        # self.player_list.update_animation()

    def is_one_of_players_dead(self):
        if self.player.is_dead or self.second_player.is_dead:
            return True
        return False

    def send_data_to_server(self, player_info):
        data = {
            "x": player_info[0],
            "y": player_info[1],
            "angle": player_info[2],
            "status": player_info[3],
            "is_dead": player_info[4],
            'id': str(self.player_id),
            'bullets': self.get_bullets()
        }
        self.ws.outbox.append(data)

    def get_bullets(self):
        bullets = []
        for i in self.bullet_list:
            bullets.append({
                'x': i.center_x,
                'y': i.center_y,
                'start_x': i.start_x,
                'start_y': i.start_y,
                'target_x': i.target_x,
                'target_y': i.target_y,
                'angle': i.angle,
                'damage': i.damage,
                'id': i.id,
                'player': self.player_id
            })

        return bullets

    def get_data_from_server(self):
        if self.ws.inbox:
            return self.ws.inbox.pop(0)
        return None

    def set_data_to_second_player(self, data):
        self.second_player.set_data(data[0], data[1], data[2], data[3], data[4])

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
