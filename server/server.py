import json

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from bullet_registration import bullet_registration

app = FastAPI()

# player_id -> websocket
connections = {}

# player_id -> player data
players = {}

bullets = {}


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(ws: WebSocket, player_id: str):
    await ws.accept()
    connections[player_id] = ws

    # начальные данные
    players[player_id] = {
        "x": 100,
        "y": 100,
        "angle": 0,
        "status": True,
        "is_dead": False,
        "bullets": [],
        "health": 100,
    }

    print(f"Player connected: {player_id}")
    print(players)

    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            data['health'] = players[player_id]['health']
            data['is_dead'] = players[player_id]['is_dead']
            # сохраняем данные игрока
            players[player_id] = data

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
                    hit_players = await bullet_registration(bullet, players)

                    print(hit_players)

                    for j in hit_players:
                        players[j]['health'] -= bullet['damage']
                        if players[j]['health'] <= 0:
                            players[j]['is_dead'] = True

                    print('---------')

            # отправляем данные других игроков
            for pid, pws in connections.items():
                await pws.send_text(json.dumps(data))

    except WebSocketDisconnect:
        print(f"Player disconnected: {player_id}")
        connections.pop(player_id, None)
        players.pop(player_id, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
