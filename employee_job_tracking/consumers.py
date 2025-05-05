import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AdminCustomerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_customer", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_customer", self.channel_name)

    async def user_create(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def user_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


class AdminJobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_jobs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_jobs", self.channel_name)

    async def job_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
