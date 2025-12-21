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
        "x": 0,
        "y": 0,
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

            # сохраняем данные игрока
            players[player_id] = data

            print('--------')
            print(data)
            print(msg)
            print(players)
            print(player_id)
            print(players[player_id])
            print('--------')

            if players[player_id]["bullets"] != [] and len(players) > 1:
                bullets_player = players[player_id]["bullets"]

                for i in bullets_player:
                    global bullets
                    if i.player not in bullets:
                        bullets[i.player] = i

                    hit_players = await bullet_registration(i['start_x'], i['start_y'], i['target_x'], i['target_y'],
                                                            players)

                    if hit_players:
                        print(hit_players)
            else:
                # global bullets

                # if bullets != {}:
                print(bullets)
                # for i in range(len(bullets)):
                #     if abs(bullets[i]['x']) > abs(bullets[i]['start_x']) + 5000 and abs(bullets[i]['y']) > abs(
                #             bullets[i]['start_y']) + 5000:
                #         bullets.pop(i)

            # отправляем данные других игроков
            for pid, pws in connections.items():
                if pid != player_id:
                    await pws.send_text(json.dumps(data))

    except WebSocketDisconnect:
        print(f"Player disconnected: {player_id}")
        connections.pop(player_id, None)
        players.pop(player_id, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
