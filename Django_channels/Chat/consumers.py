from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # print("Connected...")
        # self.send(json.dumps({
        #     'type': 'Connection_established',
        #     'message': 'Connection Established'
        # }))

    def disconnect(self, code):
        return super().disconnect(code)

    def receive(self, text_data):
        # handles the message coming from client side(html)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

        # print(message)

        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message' : message
        # }))
