import asyncio
import json
import threading

import websockets


class WSClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.ws = None

        self.inbox = []  # сообщения от сервера
        self.outbox = []  # сообщения серверу

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )
        self._thread.start()

    # -----------------------
    # asyncio loop в потоке
    # -----------------------
    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())

    async def _connect(self):
        async with websockets.connect(self.uri) as ws:
            self.ws = ws
            print("WS CONNECTED")
            print(ws)

            await asyncio.gather(
                self._sender(),
                self._receiver()
            )

    # -----------------------
    # отправка
    # -----------------------
    async def _sender(self):
        while True:
            if self.outbox:
                data = self.outbox.pop(0)
                await self.ws.send(json.dumps(data))
            await asyncio.sleep(0.01)

    # -----------------------
    # приём
    # -----------------------
    async def _receiver(self):
        async for msg in self.ws:
            self.inbox.append(json.loads(msg))
