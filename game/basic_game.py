import arcade
from arcade.gui import UIManager, UIBoxLayout, UILabel, UIAnchorLayout

from emitters import make_smoke_puff, make_explosion, make_through_blood_explosion, make_blood_puddle
from end_screen.end_screen import GameOverView
from game.game_character import Character
from variables import SCREEN_WIDTH, SCREEN_HEIGHT, ROUNDS_TO_WIN, add_hits
from variables import set_winner, add_kills, add_deaths


class BasicGame(arcade.View):
    def __init__(self, width, height, title, map_name):
        super().__init__()

        self.window.set_mouse_visible(False)
        self.window.width = width
        self.window.height = height
        self.window.title = title
        arcade.set_background_color(arcade.color.GRAY)

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_x, self.world_y = width, height

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Character(300, SCREEN_HEIGHT / 2)
        self.player_list.append(self.player)

        self.second_player = Character(SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2, True)
        self.player_list.append(self.second_player)

        self.keys_pressed = set()
        self.mouse_buttons = set()
        self.mouse_button_wheel = 0
        self.game_end = False

        self.collisions = arcade.SpriteList()

        self.tile_map = None
        self.player_physics_engine = None
        self.player_2_physics_engine = None
        self.wall_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()
        self.borrows_list = arcade.SpriteList()
        self.sand_list = arcade.SpriteList()

        self.reload_label = None
        self.reload_player_2_label = None
        self.player_health = None
        self.player_2_health = None
        self.score_1 = None
        self.score_2 = None
        self.round_text = None

        self.setup_gui()

        self.set_map(map_name)

        self.score = [0, 0]
        self.winner = 'n'
        self.round = 1
        self.setup_gui_of_game_information()

        self.emitters = []

    def setup_gui(self):
        self.manager = UIManager()
        self.manager.enable()

        self.box_layout = UIBoxLayout()  # Вертикальный стек
        self.box_layout_2 = UIBoxLayout(x=SCREEN_WIDTH - 300)

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
        self.box_layout_2.add(self.reload_player_2_label)

        self.manager.add(self.box_layout)  # Всё в manager
        self.manager.add(self.box_layout_2)  # Всё в manager

    def set_map(self, map):
        map_name = f"./map/{map}_tilemap.tmx"
        layer_options = {
            'borrows': {
                'use_spatial_hash': True
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, 1, layer_options)

        # self.collisions.append(self.second_player)

        self.wall_list = self.tile_map.sprite_lists['walls']
        self.grass_list = self.tile_map.sprite_lists['grass']
        self.sand_list = self.tile_map.sprite_lists['sand']
        self.box_list = self.tile_map.sprite_lists['box']
        self.collisions = self.tile_map.sprite_lists['collisions']

        self.player_physics_engine = arcade.PhysicsEngineSimple(self.player, self.collisions)
        self.player_2_physics_engine = arcade.PhysicsEngineSimple(self.second_player, self.collisions)

    def setup_gui_of_game_information(self):
        self.game_info = UIAnchorLayout(y=SCREEN_HEIGHT // 2 - 120)
        self.box_game_info = UIBoxLayout(vertical=True, space_between=10, x=SCREEN_WIDTH // 2 - 100,
                                         y=SCREEN_HEIGHT - 100)
        self.box_game_info_1 = UIBoxLayout(vertical=False, space_between=10, x=SCREEN_WIDTH // 2 - 100,
                                           y=SCREEN_HEIGHT - 200)

        self.score_1 = UILabel(f'{self.score[0]}', align="center", width=50, font_size=15,
                               text_color=arcade.color.RED)
        self.score_2 = UILabel(f'{self.score[0]}', align="center", width=50, font_size=15,
                               text_color=arcade.color.RED)
        self.round_text = UILabel(f'Раунд: {self.round}', align="center", width=100, font_size=12,
                                  text_color=arcade.color.RED)

        self.box_game_info_1.add(self.score_1)
        self.box_game_info_1.add(self.score_2)
        self.box_game_info.add(self.box_game_info_1)
        self.box_game_info.add(self.round_text)

        self.game_info.add(self.box_game_info)
        self.manager.add(self.game_info)

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        if self.tile_map is not None:
            self.sand_list.draw()
            self.wall_list.draw()
            self.box_list.draw()
            self.grass_list.draw()

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

        for e in self.emitters:
            e.draw()

        self.gui_camera.use()
        self.manager.draw()

        if self.game_end:
            self.win_GUI()

    def win_GUI(self):
        view = GameOverView()
        self.window.show_view(view)

    def on_update(self, delta_time: float = 1 / 60):
        if self.game_end:
            return

        self.player.update(delta_time, self.keys_pressed)
        self.second_player.update(delta_time, self.keys_pressed)

        self.handle_shoot(delta_time)

        if self.reload_label is not None:
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

        if self.player_2_physics_engine is not None:
            self.player_2_physics_engine.update()

        if self.player_health is not None:
            self.player_health.text = f'HP: {self.player.health}'
            self.player_2_health.text = f'HP: {self.second_player.health}'

        dead = self.is_one_of_players_dead()
        if dead == 1:
            self.set_score(0, 1)
        elif dead == 2:
            self.set_score(1, 0)

        if self.player_physics_engine is not None:
            self.player_physics_engine.update()
        if self.player_2_physics_engine is not None:
            self.player_2_physics_engine.update()

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

    def is_one_of_players_dead(self):
        if self.player.is_dead:
            return 1
        if self.second_player.is_dead:
            return 2
        return 0

    def bullets_check(self):
        for bullet in self.bullet_list:
            if self.second_player.is_dead or self.player.is_dead:
                continue
            collisions_first = arcade.check_for_collision(self.player, bullet)
            collisions_second = arcade.check_for_collision(self.second_player, bullet)
            is_touched_wall = arcade.check_for_collision_with_list(bullet, self.collisions)
            collision_with_bullets = arcade.check_for_collision_with_list(bullet, self.bullet_list)

            if is_touched_wall or collision_with_bullets:
                self.emitters.append(make_explosion(bullet.center_x, bullet.center_y))
                bullet.remove_from_sprite_lists()

            if collisions_second:
                add_hits(1)
                self.emitter_work_with_player(bullet)

                is_kill = self.second_player.get_damage(bullet.damage)
                if is_kill:
                    add_kills(1)
                    add_deaths(2)
                    self.second_player.remove_from_sprite_lists()

                bullet.remove_from_sprite_lists()

            if collisions_first:
                add_hits(2)
                self.emitter_work_with_player(bullet)

                is_kill = self.player.get_damage(bullet.damage)
                if is_kill:
                    add_kills(2)
                    add_deaths(1)
                    self.player.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

    def emitter_work_with_player(self, bullet):
        self.emitters.append(make_through_blood_explosion(bullet.center_x, bullet.center_y, -bullet.angle))
        blood_puddle = make_blood_puddle(bullet.center_x, bullet.center_y, count=4)
        for stain in blood_puddle:
            self.emitters.append(stain)

    def on_key_press(self, symbol, modifiers):
        self.keys_pressed.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys_pressed.remove(symbol)

    def handle_shoot(self, dt):
        if arcade.key.END in self.keys_pressed:
            bullet = self.second_player.shoot()
            if bullet is not None:
                self.bullet_list.append(bullet)
                self.emitters.append(make_smoke_puff(bullet.start_x, bullet.start_y))

        if arcade.key.SPACE in self.keys_pressed:
            bullet = self.player.shoot()
            if bullet is not None:
                self.bullet_list.append(bullet)
                self.emitters.append(make_smoke_puff(bullet.start_x, bullet.start_y))

        # For 1 player
        if arcade.key.Q in self.keys_pressed:
            self.player.angle -= 180 * dt

        if arcade.key.E in self.keys_pressed:
            self.player.angle += 180 * dt

        # For 2 player
        if arcade.key.DELETE in self.keys_pressed:
            self.second_player.angle -= 180 * dt

        if arcade.key.PAGEDOWN in self.keys_pressed:
            self.second_player.angle += 180 * dt

    def set_score(self, p1, p2):
        self.score[0] += p1
        self.score[1] += p2

        self.round += 1

        if self.score_1 is not None:
            self.score_1.text = f'{self.score[0]}'
            self.score_2.text = f'{self.score[1]}'
            self.round_text.text = f'Раунд: {self.round}'

        if self.score[0] >= ROUNDS_TO_WIN:
            self.winner = 'f'
            self.game_end = True
            set_winner('f')
        elif self.score[1] >= ROUNDS_TO_WIN:
            self.winner = 's'
            self.game_end = True
            set_winner('s')
        else:
            self.restart_round()

    def restart_round(self):
        self.player_list.clear()
        self.emitters.clear()

        self.player = Character(300, SCREEN_HEIGHT / 2 - 200)
        self.player_list.append(self.player)

        self.second_player = Character(SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2 - 200, True)
        self.player_list.append(self.second_player)
