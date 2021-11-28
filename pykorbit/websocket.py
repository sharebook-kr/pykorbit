import datetime
import websockets
import asyncio
import json
import uuid
import multiprocessing as mp


class WebSocketManager(mp.Process):
    def __init__(self, channels: list, qsize: int=1000):
        super().__init__()
        self.__q = mp.Queue(qsize)
        self.alive = False
        self.type = type
        self.channels = channels 

    async def __connect_socket(self):
        uri = "wss://ws.korbit.co.kr/v1/user/push"
        async with websockets.connect(uri, ping_interval=None) as websocket:
            now = datetime.datetime.now()
            timestamp = int(now.timestamp() * 1000)
            subscribe_fmt = {
                "accessToken": None, 
                "timestamp": timestamp, 
                "event": "korbit:subscribe",
                "data": {
                    "channels": self.channels 
                }
            }
            await websocket.send(json.dumps(subscribe_fmt))
            recv_data = await websocket.recv()
            recv_data = json.loads(recv_data)
            assert(recv_data['event'] == 'korbit:connected')

            recv_data = await websocket.recv()
            recv_data = json.loads(recv_data)
            assert(recv_data['event'] == 'korbit:subscribe')

            while self.alive:
                recv_data = await websocket.recv()
                self.__q.put(json.loads(recv_data))

    def run(self):
        self.__aloop = asyncio.get_event_loop()
        self.__aloop.run_until_complete(self.__connect_socket())

    def get(self):
        if self.alive == False:
            self.alive = True
            self.start()
        return self.__q.get()

    def terminate(self):
        self.alive = False
        super().terminate()


if __name__ == "__main__":
    # channels
    # ticker
    # orderbook
    # transation
    # https://apidocs.korbit.co.kr/ko/#2a5edfe20c 
    wm = WebSocketManager(["ticker:btc_krw"])
    for i in range(10):
        data = wm.get()
        print(data)
    wm.terminate()