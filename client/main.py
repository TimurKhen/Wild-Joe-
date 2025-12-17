import arcade

from client.game.basic_game import BasicGame
from client.variables import set_width_height


def set_up_game():
    screen_width, screen_height = arcade.get_display_size()
    set_width_height(screen_width, screen_height)

    w = BasicGame(screen_width, screen_height, 'Game')
    w.setup()
    arcade.run()


set_up_game()
