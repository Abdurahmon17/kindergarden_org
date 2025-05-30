import json
from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult
import asyncio
import logging

logger = logging.getLogger(__name__)


class ReportStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f'report_{self.task_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Start polling task status
        asyncio.create_task(self.poll_task_status())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def poll_task_status(self):
        while True:
            try:
                task = AsyncResult(self.task_id)
                status = {
                    'ready': task.ready(),
                    'successful': task.successful(),
                    'result': task.result if task.ready() else None
                }
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'task_update',
                        'status': status
                    }
                )
                if task.ready():
                    break
            except Exception as e:
                logger.error(f"Error polling task {self.task_id}: {e}")
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'task_update',
                        'status': {'error': str(e)}
                    }
                )
                break
            await asyncio.sleep(2)

    async def task_update(self, event):
        await self.send(text_data=json.dumps(event['status']))