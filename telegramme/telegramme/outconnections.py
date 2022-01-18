import json
import datetime
import websocket
import _thread
import time

from telegramme import models 
from telegramme.tools import register_message, register_message_sync


class OutConnection:
    @staticmethod
    def on_message(ws, message):
        print('message in outconnections')
        message = json.loads(message)

        register_message_sync(
            content=message.get('message').get('text'),
            received=True,
            datetime=datetime.datetime.now()
        )

        print(message)

    @staticmethod
    def on_error(ws, error):
        print(error)

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        print("### closed ###")

    @staticmethod
    def on_open(ws, *args):
        # sync
        print("### closed ###")

    def __init__(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://127.0.0.1:9000/ws/chat/",
                                  on_open=OutConnection.on_open,
                                  on_message=OutConnection.on_message,
                                  on_error=OutConnection.on_error,
                                  on_close=OutConnection.on_close)
        self.ws = ws
        _thread.start_new_thread(ws.run_forever, ())


class OutConnectionSignleton:
    connection = OutConnection()
