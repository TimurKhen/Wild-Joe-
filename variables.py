SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


def set_width_height(width, height):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height


ROUNDS_TO_WIN = 10
SHOW_HITBOX = False
MAP_SETTINGS = {
    'name': 'joe'
}
PLAYERS_STATISTICS = {
    1:
        {
            "kills": 0,
            "deaths": 0,
            "shots_count": 0,
            "hits": 0,
        },
    2:
        {
            "kills": 0,
            "deaths": 0,
            "shots_count": 0,
            "hits": 0,
        },
    "winner": ''
}


def add_kills(player):
    global PLAYERS_STATISTICS

    PLAYERS_STATISTICS[player]['kills'] += 1


def add_deaths(player):
    global PLAYERS_STATISTICS

    PLAYERS_STATISTICS[player]['deaths'] += 1


def add_shots(player):
    global PLAYERS_STATISTICS
    pass
    PLAYERS_STATISTICS[player]['shots_count'] += 1


def add_hits(player):
    global PLAYERS_STATISTICS

    PLAYERS_STATISTICS[player]['hits'] += 1


def set_winner(player):
    global PLAYERS_STATISTICS

    PLAYERS_STATISTICS['winner'] = player


def restore_data():
    global PLAYERS_STATISTICS

    PLAYERS_STATISTICS[1] = {
        "kills": 0,
        "deaths": 0,
        "shots_count": 0,
        "hits": 0,
    }
    PLAYERS_STATISTICS[2] = {
        "kills": 0,
        "deaths": 0,
        "shots_count": 0,
        "hits": 0,
    }
    PLAYERS_STATISTICS['winner'] = ''
