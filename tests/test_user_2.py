import asyncio
import json

import websockets


async def run():
    uri = "ws://127.0.0.1:8000/ws/player2"

    async with websockets.connect(uri) as ws:
        print("PLAYER 2 CONNECTED")

        async def sender():
            y = 0
            while True:
                y += 5
                data = {
                    "x": 200,
                    "y": y,
                    "angle": 90,
                    "status": True,
                    "is_dead": False
                }
                await ws.send(json.dumps(data))
                print("PLAYER 2 SENT:", data)
                await asyncio.sleep(1)

        async def receiver():
            async for msg in ws:
                print("PLAYER 2 RECEIVED:", json.loads(msg))

        await asyncio.gather(sender(), receiver())


asyncio.run(run())
