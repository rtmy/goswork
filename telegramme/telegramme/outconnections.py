import json
import datetime
import websocket
import _thread
import time

from telegramme import models 
from telegramme.tools import register_message, register_message_sync


class OutConnection:
    """Класс отправки сообщений с различными обработчиками для режима клиента"""

    @staticmethod
    def on_message(ws, message):
        print('message in outconnections')
        message = json.loads(message)

        register_message_sync(
            content=message.get('message'),
            received=True,
            datetime=datetime.datetime.now()
        )

        print(message)

    @staticmethod
    def on_error(ws, error):
        print(error)

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        with open('statefile', 'w') as file:
            file.write('0')
        print("### closed ###")

    @staticmethod
    def on_open(ws, *args):
        # Todo: sync
        
        with open('statefile', 'w') as file:
            file.write('node')
        print("### closed ###")

    def __init__(self, address='127.0.0.1:9000'):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(f'ws://{address}/ws/chat/',
                                  on_open=OutConnection.on_open,
                                  on_message=OutConnection.on_message,
                                  on_error=OutConnection.on_error,
                                  on_close=OutConnection.on_close)
        self.ws = ws
        _thread.start_new_thread(ws.run_forever, ())


class OutConnectionSignleton:
    """Singleton - оборачивание класса вебсокетера в переменную класса"""
    connection = OutConnection()
