import arcade
from arcade.gui import UIManager, UIBoxLayout, UILabel, UIAnchorLayout

from client.variables import PLAYERS_STATISTICS, SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.title = 'Game Over'
        self.window.default_camera.use()
        self.lidder_board = self.load_lidder_board()

        self.manager = UIManager()
        self.manager.enable()

        self.anchor = UIAnchorLayout()
        self.main_layout = UIBoxLayout(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2, vertical=True, space_between=20)
        self.set_up_ui()

    def load_lidder_board(self):
        lines = []
        with open('./client/records.txt', 'r') as f:
            lines = list(map(lambda x: x.strip().split(':'), f.readlines()))

        return lines

    def replace_line_in_file(self, line_number, new_line_content):
        if not new_line_content.endswith('\n'):
            new_line_content += '\n'

        with open('./client/records.txt', 'r') as file:
            lines = file.readlines()

        lines[line_number] = new_line_content

        with open('./client/records.txt', 'w') as file:
            file.writelines(lines)

    def check_with_lidder_board(self, player_data, another_player_data):
        output = []

        if player_data['kd'] > float(self.lidder_board[0][1]) and player_data['kd'] > another_player_data['kd']:
            self.replace_line_in_file(0, f'bestKD:{player_data["kd"]}')
            output.append(1)
        if player_data['acc'] > float(self.lidder_board[1][1]) and player_data['kd'] > another_player_data['kd']:
            self.replace_line_in_file(1, f'bestACC:{player_data["acc"]}')
            output.append(2)

        return output

    def convert_player_data(self, player_data):
        kills = player_data[0]
        deaths = max(player_data[1], 1)
        shots = max(player_data[2], 1)
        hits = player_data[3]

        output = {
            'kd': round(kills / deaths, 2),
            'acc': round(hits / shots, 2),
        }

        return output

    def set_up_ui(self):
        player_1 = self.convert_player_data([
            PLAYERS_STATISTICS[1]['kills'],
            PLAYERS_STATISTICS[1]['deaths'],
            PLAYERS_STATISTICS[1]['shots_count'],
            PLAYERS_STATISTICS[1]['hits'],
        ])

        player_2 = self.convert_player_data([
            PLAYERS_STATISTICS[2]['kills'],
            PLAYERS_STATISTICS[2]['deaths'],
            PLAYERS_STATISTICS[2]['shots_count'],
            PLAYERS_STATISTICS[2]['hits'],
        ])
        winner = PLAYERS_STATISTICS['winner']

        player_1_lidderboard_check = self.check_with_lidder_board(player_1, player_2)
        player_2_lidderboard_check = self.check_with_lidder_board(player_2, player_1)

        if not player_1_lidderboard_check:
            pass
        if not player_2_lidderboard_check:
            pass

        if winner == 'f':
            winner = '1'
        elif winner == 's':
            winner = '2'

        winner_label = UILabel(text=f'Победил игрок: {winner}', font_size=20, text_color=arcade.color.BLACK)

        data_of_player_1 = UILabel(
            text=f"P1: KD: {player_1['kd']}, acc: {player_1['acc']}",
            font_size=20,
            align="center",
            width=500, text_color=arcade.color.BLACK
        )

        data_of_player_2 = UILabel(
            text=f"P2: KD: {player_2['kd']}, acc: {player_2['acc']}",
            font_size=20,
            align="center",
            width=500, text_color=arcade.color.BLACK
        )

        key = {
            1: 'kd',
            2: 'acc',
        }
        self.main_layout.add(winner_label)
        self.main_layout.add(data_of_player_1)
        self.main_layout.add(data_of_player_2)

        if 1 in player_1_lidderboard_check:
            lidder_board_message_1 = UILabel(
                text=f"Игрок 1 поставил новый рекорд! по {key[1]} - {player_1[key[1]]}",
                font_size=25,
                align="center",
                width=500, text_color=arcade.color.BLACK
            )
            self.main_layout.add(lidder_board_message_1)

        if 2 in player_1_lidderboard_check:
            lidder_board_message_1 = UILabel(
                text=f"Игрок 1 поставил новый рекорд! по {key[1]} - {player_1[key[1]]}",
                font_size=25,
                align="center",
                width=500, text_color=arcade.color.BLACK
            )
            self.main_layout.add(lidder_board_message_1)

        if 1 in player_2_lidderboard_check:
            lidder_board_message_2 = UILabel(
                text=f"Игрок 2 поставил новый рекорд! по {key[1]} - {player_2[key[1]]}",
                font_size=25,
                align="center",
                width=500, text_color=arcade.color.BLACK
            )
            self.main_layout.add(lidder_board_message_2)

        if 2 in player_2_lidderboard_check:
            lidder_board_message_2 = UILabel(
                text=f"Игрок 2 поставил новый рекорд! по {key[2]} - {player_2[key[2]]}",
                font_size=25,
                align="center",
                width=500, text_color=arcade.color.BLACK
            )
            self.main_layout.add(lidder_board_message_2)

        self.anchor.add(self.main_layout)
        self.manager.add(self.anchor)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
