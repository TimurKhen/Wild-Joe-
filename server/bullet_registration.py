async def bullet_registration(x, y, hitbox_size, players_list):
    hit_players = []

    for player_id, player_data in players_list.items():
        player_x = player_data["x"]
        player_y = player_data["y"]

        if player_x - hitbox_size < x < player_x + hitbox_size and player_y - hitbox_size < y < player_y + hitbox_size:
            hit_players.append(player_id)

    return hit_players
