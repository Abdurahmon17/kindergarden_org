from channels.generic.websocket import AsyncWebsocketConsumer
import json

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        self.group_name = 'stock_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    async def low_stock_alert(self, event):
        await self.send(text_data=json.dumps({
            'type': 'low_stock_alert',
            'message': event['message']
        }))
    async def report_warning(self, event):
        await self.send(text_data=json.dumps({
            'type': 'report_warning',
            'message': event['message']
        }))