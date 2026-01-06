import json
import time

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from bullet_registration import bullet_registration

app = FastAPI()

# player_id -> websocket
connections = {}

# player_id -> player data
players = {}

hitted_bullets = []

is_game_running = False


# TODO
#  Выбор карты

async def cleaner():
    if len(hitted_bullets) == 0:
        return

    current_time = time.time()
    for i in range(len(hitted_bullets)):
        if len(hitted_bullets) >= i:
            try:
                if current_time - hitted_bullets[i][1] > 3.0:
                    hitted_bullets.pop(i)
            except IndexError as e:
                print(e)


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(ws: WebSocket, player_id: str):
    global is_game_running

    if len(players) >= 2:
        return
    else:
        await ws.accept()
    connections[player_id] = ws

    # начальные данные
    # players[player_id] = {
    #     "x": random.randint(100, 1820),
    #     "y": random.randint(100, 980),
    #     "angle": 0,
    #     "status": True,
    #     "is_dead": False,
    #     "bullets": [],
    #     "health": 100,
    # }

    print(f"Player connected: {player_id}")
    print(players)

    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            players[player_id] = data
            # data['health'] = players[player_id]['health']
            # data['is_dead'] = players[player_id]['is_dead']
            # сохраняем данные игрока
            # players[player_id] = data

            # print('--------')
            # print(data)
            # print(players)
            # print(player_id)
            # print(players[player_id])

            player_bullets = data["bullets"]

            if len(players) > 1:
                # print('player_count > 0')
                # print('player_count > 0')
                # print('player_count > 0')
                # print('player_count > 0')
                # print('player_count > 0')
                # print(player_bullets)
                # print(player_bullets)
                # print(player_bullets)
                # print(player_bullets)

                for i in range(len(player_bullets)):
                    bullet = player_bullets[i]
                    bullet = json.loads(bullet)
                    print(bullet)
                    print(players)

                    if bullet['id'] not in hitted_bullets:
                        hit_players = await bullet_registration(bullet, players)

                        if len(hit_players) > 0:
                            hitted_bullets.append([bullet['id'], time.time()])

                        for j in hit_players:
                            players[j]['health'] -= bullet['damage']
                            if players[j]['health'] <= 0:
                                players[j]['is_dead'] = True

                    print('---------')

                await cleaner()

            # отправляем данные других игроков
            for pid, pws in connections.items():
                await pws.send_text(json.dumps(data))

    except WebSocketDisconnect:
        print(f"Player disconnected: {player_id}")
        connections.pop(player_id, None)
        players.pop(player_id, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
