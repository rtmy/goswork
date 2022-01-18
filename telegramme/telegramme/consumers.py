import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        ...

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Send message to room group
        print('got here', text_data)
        await self.send(json.dumps(
            {
                'type': 'chat_message',
                'message': 'ans',
            }
        ))
