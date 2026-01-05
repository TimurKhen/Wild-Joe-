async def bullet_registration(bullet, players_list):
    hit_players = set()

    bullet_x = bullet['x']
    bullet_y = bullet['y']
    bullet_hitbox = bullet['hitbox_size']
    bullet_owner = bullet['player']

    # print(players_list)

    for i in players_list:
        if i == bullet_owner:
            continue

        player = players_list[i]
        player_x = player['x']
        player_y = player['y']
        pr = 60

        if player_x - pr <= bullet_x <= player_x + pr and player_y - pr <= bullet_y <= player_y + pr:
            hit_players.add(i)

    return hit_players
