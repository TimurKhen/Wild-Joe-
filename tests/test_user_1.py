import asyncio
import json
import uuid

import websockets


async def run():
    uri = f"ws://127.0.0.1:8000/ws/{uuid.uuid4()}"

    async with websockets.connect(uri) as ws:
        print("PLAYER 1 CONNECTED")

        async def sender():
            x = 0
            while True:
                x += 10
                data = {
                    "x": x,
                    "y": 100,
                    "angle": 0,
                    "status": True,
                    "is_dead": False,
                    'id': str(ws.id)
                }
                await ws.send(json.dumps(data))
                print("PLAYER 1 SENT:", data)
                await asyncio.sleep(1)

        async def receiver():
            async for msg in ws:
                print("PLAYER 1 RECEIVED:", json.loads(msg), dir(ws))

        await asyncio.gather(sender(), receiver())


asyncio.run(run())
