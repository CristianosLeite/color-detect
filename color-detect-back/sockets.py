import asyncio
import websockets

class WebsocketServer:
    def __init__(self, tfc01):
        self.tfc01 = tfc01

    async def camera_status(self, websocket):
        while True:
            status = str(self.tfc01.cam_run)
            await websocket.send(status)
            await asyncio.sleep(1)

    async def plc_status(self, websocket):
        while True:
            status = str(self.tfc01.get_plc_status())
            await websocket.send(status)
            await asyncio.sleep(1)

    async def api_status(self, websocket):
        while True:
            status = str(self.tfc01.api_status)
            await websocket.send(status)
            await asyncio.sleep(1)

    async def start_server(self):
        server1 = websockets.serve(self.camera_status, "localhost", 8765)
        server2 = websockets.serve(self.plc_status, "localhost", 8766)
        server3 = websockets.serve(self.api_status, "localhost", 8767)

        async def infinite_loop():
            while True:
                await asyncio.sleep(1)

        await asyncio.gather(server1, server2, server3, infinite_loop())


if __name__ == '__main__':
    ws = WebsocketServer()
    asyncio.run(ws.start_server())
