import os
import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from telegramme.tools import register_message


class ChatConsumer(AsyncWebsocketConsumer):
    """Класс отправки сообщений с различными обработчиками для режима сервера"""
    
    # Receive message from room group
    async def chat_message(self, event):
        """Метод приема сообщений от внутренней шины (redis)"""
        print('RECEIVED MESSAGE TO SEND', event)
        
        await register_message(
            content=event['text'],
            received=False,
            datetime_received=datetime.datetime.now()
        )

        await self.send(text_data=json.dumps({
            'message': event['text']
        }))

    async def connect(self):
        print('channel name', self.channel_name)
        with open('channel_name', 'w') as file:
            file.write(self.channel_name)
        with open('statefile', 'w') as file:
            file.write('master')
        await self.accept()

    async def disconnect(self, close_code):
        with open('statefile', 'w') as file:
            file.write('0')

    async def receive(self, text_data):
        if text_data != 'init_announcement':
            await register_message(
                content=text_data,
                received=True,
                datetime_received=datetime.datetime.now()
            )
