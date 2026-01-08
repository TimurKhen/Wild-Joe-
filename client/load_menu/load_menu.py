import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

from client import variables
from client.game.basic_game import BasicGame
from client.variables import SCREEN_HEIGHT, SCREEN_WIDTH


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = None
        self.anchor_layout = None
        self.box_layout = None

    def on_show_view(self):
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.create_ui_elements()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def create_ui_elements(self):
        label = UILabel(
            text="Shooter game",
            font_size=20,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        self.box_layout.add(label)

        maps = [
            {"text": "Карта 1", "name": "joe"},
            {"text": "Карта 2", "name": "inf"},
        ]

        for map_info in maps:
            self.create_map_button(map_info["text"], map_info["name"])

    def create_map_button(self, button_text, map_name):
        button = UIFlatButton(
            text=button_text,
            width=200,
            height=50,
            color=arcade.color.BLUE
        )
        button.map_name = map_name
        button.on_click = self.on_map_selected
        self.box_layout.add(button)

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
