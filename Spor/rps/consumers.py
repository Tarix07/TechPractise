from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import JsonWebsocketConsumer
import json
from .models import Game, Profile
from django.core import serializers

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
           # async_to_sync(self.channel_layer.group_send)(
            #    self.room_group_name,
            #    {
            #        'type': 'users_message',
            #        'message': '2players',
            #        'creator': game.creator.username,
            #        'opponent': game.opponent.username
            #    }
            #)

        if game.opponent is None and me.id != game.creator.id:
            game.set_opponent(me)

        if game.creator is not None and game.opponent is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'users_message',
                    'message': '2players',
                    'creator': game.creator.username,
                    'opponent': game.opponent.username
                }
            )

        self.accept()

    def users_message(self, event):
        message = event['message']
        creator = event['creator']
        opponent = event['opponent']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'creator': creator,
            'opponent': opponent
        }))

    def disconnect(self, close_code):
        # Leave room group
        game = Game.get_game(self.scope['url_route']['kwargs']['room_name'])

        me = self.scope['user']
        if me == game.opponent and game.opponent_choice is None:
            game.opponent = None
            game.set_status("waiting")
            game.save()

        if me == game.creator and game.creator_choice is None:
            game.creator = None
            game.set_status("waiting")
            game.save()

        #if game.opponent_choice is None:
        #    game.opponent = None
        #    game.set_status("waiting")
        #    game.save()

        #if game.creator_choice is None:
        #    game.creator = None
        #    game.set_status("waiting")
        #    game.save()


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'users_message',
                'message': 'waiting',
                'creator': "",
                'opponent': ""
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        me = self.scope['user']
        game = Game.get_game(self.scope['url_route']['kwargs']['room_name'])

        if me.username == game.creator.username:
            game.make_creator_choice(message)

        elif me.username == game.opponent.username:
            game.make_opponent_choice(message)

        result = ""

        if game.creator_choice is not None and game.opponent_choice is not None:
            result = game.result()

        profile = Profile.get_profile(me)

        winner = ""
        isCompleted=""
        if game.winner is not None:
            winner = game.winner.username
            isCompleted="completed"
            if game.creator.username == winner:
                profile.change_profile(game.creator, 1)
                profile.change_profile(game.opponent, 0)
            else:
                profile.change_profile(game.creator, 0)
                profile.change_profile(game.opponent, 1)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': isCompleted,
                'username': me.username,
                'winner': winner,
                'result': result
                }
            )



    # Receive message from room group
    def game_message(self, event):
        message = event['message']
        username = event['username']
        winner = event['winner']
        result = event['result']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'winner': winner,
            'result': result
        }))

    def close_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))

class LobbyConsumer(WebsocketConsumer):
        def connect(self):
            self.room_group_name = "lobby"
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

        def disconnect(self, close_code):
            pass

        def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            me = self.scope['user']
            action = text_data_json['action']
            if action == "random":
                randomGame = ""
                if Game.get_available_games().count() != 0:
                    randomGame = Game.get_random().game_name

                self.send(text_data=json.dumps({
                    'type': 'response_message',
                    'message': "random",
                    'randomgame': randomGame
                }))

            if action == "create":
                game = Game.objects.filter(game_name=message)

                if game.exists():
                    message = "deny"
                else:
                    game = Game.create_new(message,  me)
                    message = "accept"

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'game_message',
                            'message': "new_game",
                            'username': game.creator.username,
                            'name': game.game_name

                        }
                    )


                #dani =Game.objects.filter(status__exact="waiting").order_by('game_name')[:20]
                #print(dani)

                #for i in dani:
                    #print(i.game_name)
                #dani = serializers.serialize('json', dani, fields=('game_name','creator'))
                self.send(text_data=json.dumps({
                    'type': 'response_message',
                    'message': message,
                }))



        # Receive message from room group
        def game_message(self, event):
            message = event['message']
            username = event['username']
            name = event['name']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'name': name
            }))

        def response_message(self, event):
            message = event['message']
            game_name=event['game_name']
            game_creator=event['game_creator']
            randomgame = event['']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'game_name': game_name,
                'game_creator': game_creator
            }))