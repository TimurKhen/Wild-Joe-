import arcade

from client.load_menu.load_menu import StartView
from client.variables import set_width_height


def set_up_game():
    screen_width, screen_height = arcade.get_display_size()
    set_width_height(screen_width, screen_height)
    # screen_width, screen_height = 1000, 600
    window = arcade.Window(800, 600, "Моя Игра")
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == '__main__':
    set_up_game()
