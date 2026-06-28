import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from employee_job_tracking.models import Message , CustomUser
from channels.db import database_sync_to_async
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
  # Make sure it's importing correctly

class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     print("📡 WebSocket connect initiated.")
    #     from urllib.parse import parse_qs
    #     from app.helper import user_validation

    #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name = f'chat_{self.room_name}'
    #     query_string = self.scope['query_string'].decode()
    #     query_params = parse_qs(query_string)
    #     token = query_params.get('token', [None])[0]
    #     user = user_validation(token)
    #     user_json = user_validation(token)
    #     if user_json["message"] == "User present":   
    #         user = user_json["user_obj"]
    #     sender = user.id
    #     print(f"🛏 Room name: {self.room_name}")
    #     print(f"👥 Room group name: {self.room_group_name}")

    #     # Add to room group (optional/general use)
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     print("✅ Added to room group.")

    #     # Add to user-specific group (hardcoded user id 17)
    #     self.user_id = sender
    #     self.user_group_name = f'user_{self.user_id}'
    #     await self.channel_layer.group_add(
    #         self.user_group_name,
    #         self.channel_name
    #     )
    #     print(f"✅ Added to user group: {self.user_group_name}")

    #     await self.accept()
    #     print("✅ WebSocket connection accepted.")

    async def connect(self):
        from urllib.parse import parse_qs
        from asgiref.sync import sync_to_async
        from app.helper import user_validation
        print("📡 WebSocket connect initiated.")

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Get token from URL
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if not token:
            print("❌ Token missing.")
            await self.close()
            return

        # Safely call the sync function inside async code
        user_json = await sync_to_async(user_validation)(token)

        if user_json["message"] != "User present":
            print("❌ Invalid token or user not found.")
            await self.close()
            return

        user = user_json["user_obj"]
        sender = user.id
        print( "sender id is ",sender)

        print(f"🛏 Room name: {self.room_name}")
        print(f"👥 Room group name: {self.room_group_name}")

        # Add to room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print("✅ Added to room group.")

        self.user_id = sender
        self.user_group_name = f'user_{self.user_id}'
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        print(f"✅ Added to user group: {self.user_group_name}")

        await self.accept()
        print("✅ WebSocket connection accepted.")
    async def disconnect(self, close_code):
        print(f"🔌 Disconnecting... close_code: {close_code}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("✅ Disconnected from room group.")

        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        print(f"✅ Disconnected from user group: {self.user_group_name}")

    async def receive(self, text_data):
        print("📩 Message received via WebSocket.")
        print(f"📦 Raw data: {text_data}")

        from employee_job_tracking.models import Message, CustomUser

        data = json.loads(text_data)
        print(f"🧹 Parsed JSON: {data}")

        # Use hardcoded user ID 17 for sender
        sender = data.get('sender_id')
        user = await self.get_user(sender)
        # print(f"👤 Sender user: {user} (ID: {user.id})")

        message_type = data.get('message_type', 'text')
        content = data.get('content', '')
        receiver_id = data.get('receiver_id')

        print(f"📝 Message content: '{content}' | Type: '{message_type}' | Receiver ID: {receiver_id}")

        if receiver_id:
            receiver = await self.get_user(receiver_id)
            print(f"🎯 Receiver user: {receiver} (ID: {receiver.id})")
        else:
            print("⚠️ No receiver_id provided.")

        message = await self.save_message(user, receiver, message_type, content)
        print(f"💾 Message saved in DB with ID: {message.id}")

        if receiver:
            receiver_group = f'user_{receiver.id}'
            await self.channel_layer.group_send(
                receiver_group,
                {
                    'type': 'chat_message',
                    'message': content,
                    'sender_id': user.id,
                    'receiver_id': receiver.id,
                    'message_type': message_type,
                }
            )
            print(f"📤 Message sent to receiver group: {receiver_group}")

        # Optionally, send message back to sender too
        sender_group = f'user_{user.id}'
        await self.channel_layer.group_send(
            sender_group,
            {
                'type': 'chat_message',
                'message': content,
                'sender_id': user.id,
                'receiver_id': receiver.id if receiver else None,
                'message_type': message_type,
            }
        )
        print(f"📤 Message echoed back to sender group: {sender_group}")

    async def chat_message(self, event):
        print(f"📬 Sending message to WebSocket client: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'message_type': event['message_type'],
        }))
        print("✅ Message sent to WebSocket.")

    @database_sync_to_async
    def save_message(self, sender, receiver, message_type, content, media_file=None):
        print("💽 Saving message to database...")
        from employee_job_tracking.models import Message
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            content=content,
            # media_file=media_file,
        )
        print(f"✅ Message created: {message}")
        return message

    @database_sync_to_async
    def get_user(self, user_id):
        print(f"🔍 Fetching CustomUser with ID: {user_id}")
        from employee_job_tracking.models import CustomUser
        user = CustomUser.objects.get(id=user_id)
        print(f"✅ Fetched user: {user}")
        return user
