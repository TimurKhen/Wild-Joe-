import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

from client.game.basic_game import BasicGame
from client.variables import SCREEN_HEIGHT, SCREEN_WIDTH, set_map


class StartView(arcade.View):
    def on_show_view(self):
        super().__init__()
        self.setup()

    def setup(self):
        """Настройка начального экрана"""
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        self.set_text()
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def set_text(self):
        label = UILabel(text="Shooter game",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        flat_button = UIFlatButton(text="Карта 1", width=200, height=50, color=arcade.color.BLUE)
        flat_button.on_click = self.map_select_1
        self.box_layout.add(flat_button)

        flat_button = UIFlatButton(text="Карта 2", width=200, height=50, color=arcade.color.BLUE)
        flat_button.on_click = self.map_select_2
        self.box_layout.add(flat_button)

    def on_draw(self):
        """Отрисовка начального экрана"""
        self.clear()
        # Батч для текста
        self.manager.draw()

    def map_select_1(self, event):
        set_map('joe')
        self.start_game(event)

    def map_select_2(self, event):
        set_map('joe')
        self.start_game(event)

    def start_game(self, event):
        print('start')
        """Начало игры при нажатии клавиши"""
        w = BasicGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game')
        # w.setup()
        self.window.show_view(w)
