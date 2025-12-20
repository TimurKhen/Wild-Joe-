import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

# player_id -> websocket
connections = {}

# player_id -> player data
players = {}


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
        "is_dead": False
    }

    print(f"Player connected: {player_id}")

    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)

            # сохраняем данные игрока
            players[player_id] = data

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