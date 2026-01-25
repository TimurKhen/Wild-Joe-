import arcade

from client.load_menu.load_menu import StartView
from client.variables import set_width_height


def set_up_game():
    screen_width, screen_height = arcade.get_display_size()
    set_width_height(screen_width, screen_height)
    # screen_width, screen_height = 1000, 600
    window = arcade.Window(1000, 600, "Evil Joe")
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


def restore_records():
    with open('./records.txt', 'w') as f:
        f.write('bestKD:0.0\n')
        f.write('bestACC:0.0')
        f.close()


if __name__ == '__main__':
    # restore_records()
    set_up_game()
