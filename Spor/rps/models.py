from builtins import staticmethod
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Game(models.Model):
    game_name = models.TextField(max_length=50, unique=True, blank=True)
    winner = models.ForeignKey(
        User, related_name='winner', null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        User, related_name='opponent', null=True, blank=True, on_delete=models.CASCADE)
    completed = models.DateTimeField(null=True, blank=True)
    creator_choice = models.TextField(null=True, blank=True,)
    opponent_choice = models.TextField(null=True, blank=True)
    status = models.TextField(blank=True, default="waiting")


    @staticmethod
    def create_new(name, user):
        new_game = Game(creator=user, game_name=name)
        new_game.save()
        return new_game

    def set_creator(self, user):
        self.creator = User.objects.filter(username=user)[0]
        self.save(update_fields=["creator"])

    def set_opponent(self, user):
        self.opponent = User.objects.filter(username=user)[0]
        self.set_status("running")
        self.save(update_fields=["opponent"])

    def set_status(self, status):
        self.status = status
        self.save(update_fields=["status"])

    def __str__(self):
        return self.game_name

    @staticmethod
    def get_game(name):
        game = Game.objects.filter(game_name__exact=name)
        if game.exists():
            game = game.first()
        return game

    def mark_complete(self, winner):
        self.winner = winner
        self.completed = datetime.now()
        self.set_status("completed")
        self.save()

    def result(self):
        if self.creator_choice == 'rock' and self.opponent_choice == 'scissors':
            self.mark_complete(self.creator)
        elif self.creator_choice == 'scissors' and self.opponent_choice == 'paper':
            self.mark_complete(self.creator)
        elif self.creator_choice == 'paper' and self.opponent_choice == 'rock':
            self.mark_complete(self.creator)
        elif self.opponent_choice == 'rock' and self.creator_choice == 'scissors':
            self.mark_complete(self.opponent)
        elif self.opponent_choice == 'scissors' and self.creator_choice == 'paper':
            self.mark_complete(self.opponent)
        elif self.opponent_choice == 'paper' and self.creator_choice == 'rock':
            self.mark_complete(self.opponent)
        elif self.opponent_choice == self.creator_choice:
            self.opponent_choice = ""
            self.creator_choice = ""
            self.save(update_fields=["opponent_choice", "creator_choice"])
            return "tai"

    def make_creator_choice(self, message):
        self.creator_choice = message
        self.save(update_fields=["creator_choice"])

    def make_opponent_choice(self, message):
        self.opponent_choice = message
        self.save(update_fields=["opponent_choice"])

    @staticmethod
    def get_available_games():
        return Game.objects.filter(status__exact="waiting").order_by('game_name')[:20]

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user) | Q(creator=user))

    @staticmethod
    def get_completed_games():
        return Game.objects.filter(status="completed").order_by('completed')

