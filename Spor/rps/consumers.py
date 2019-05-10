from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Game

class GameConsumer(WebsocketConsumer):


   def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        me = self.scope['user']

        game = Game.get_game(self.scope['url_route']['kwargs']['room_name'])
        if game.status == "completed":
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'close_message',
                'message': "closed"
            })


        if game.creator is None:
            game.set_creator(me)
        if game.opponent is None and me.id != game.creator.id:
            game.set_opponent(me)


        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

      
    def close_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))