import os
import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from telegramme.tools import register_message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('channel name', self.channel_name)
        with open('channel_name', 'w') as file:
            file.write(self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        ...

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Send message to room group
        await register_message(
            content=text_data,
            received=True,
            datetime_received=datetime.datetime.now()
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('RECEIVED MESSAGE TO SEND', event)
        
        await register_message(
            content=event['text'],
            received=False,
            datetime_received=datetime.datetime.now()
        )

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['text']
        }))
