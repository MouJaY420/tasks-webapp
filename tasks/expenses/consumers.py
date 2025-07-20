import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ReceiptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.household_id = self.scope['url_route']['kwargs']['household_id']
        self.group_name = f'receipt_{self.household_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'receipt_uploaded',
                'text': text_data
            }
        )

    async def receipt_uploaded(self, event):
        await self.send(text_data=event["text"])
