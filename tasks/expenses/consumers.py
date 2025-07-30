# expenses/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ReceiptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.household_id = self.scope['url_route']['kwargs']['household_id']
        self.group_name = f"receipt_updates_{self.household_id}"
        print(f"WebSocket connection received for household {self.household_id}")

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_receipt_update(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
