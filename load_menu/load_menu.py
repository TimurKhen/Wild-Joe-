import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton, UIImage

import variables
from game.basic_game import BasicGame
from variables import restore_data
from variables import SCREEN_HEIGHT, SCREEN_WIDTH


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = None
        self.anchor_layout = None
        self.main_layout = None
        self.left_image = None
        self.right_image = None
        restore_data()

    def on_show_view(self):
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.REDWOOD)

        self.manager = UIManager()
        self.manager.enable()

        self.main_layout = UIBoxLayout(vertical=False, space_between=20)

        self.left_texture = arcade.load_texture('./textures/player1_controls.png')
        self.right_texture = arcade.load_texture('./textures/player2_controls.png')

        left_image_widget = UIImage(
            texture=self.left_texture,
            width=300,
            height=300
        )

        right_image_widget = UIImage(
            texture=self.right_texture,
            width=300,
            height=300
        )

        center_container = UIBoxLayout(vertical=True, space_between=10)

        self.main_layout.add(left_image_widget)
        self.main_layout.add(center_container)
        self.main_layout.add(right_image_widget)

        self.create_ui_elements(center_container)

        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout.add(self.main_layout)
        self.manager.add(self.anchor_layout)

    def create_ui_elements(self, container):
        label = UILabel(
            text="Shooter game",
            font_size=20,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        container.add(label)

        maps = [
            {"text": "Карта 1", "name": "joe"},
            {"text": "Карта 2", "name": "inf"},
            {"text": "Пустая карта", "name": "white"},
        ]

        for map_info in maps:
            self.create_map_button(container, map_info["text"], map_info["name"])

    def create_map_button(self, container, button_text, map_name):
        button = UIFlatButton(
            text=button_text,
            width=300,
            height=50,
            color=arcade.color.RED
        )
        button.map_name = map_name
        button.on_click = self.on_map_selected
        container.add(button)

    def on_map_selected(self, event):
        map_name = event.source.map_name
        self.start_game(map_name)

    def start_game(self, map_name):
        variables.MAP_SETTINGS['name'] = map_name
        game_view = BasicGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game', map_name)
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
