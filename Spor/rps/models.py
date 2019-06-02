from django.contrib.auth.models import User
from django.db import models
import json
from datetime import datetime


class Game(models.Model):
    game_name = models.TextField(max_length=50, unique=True, blank=True)
    winner = models.ForeignKey(
        User, related_name='winner', null=True, blank=True, on_delete=models.DO_NOTHING)
    creator = models.ForeignKey(
        User, null=True,blank=True, related_name='creator', on_delete=models.DO_NOTHING)
    opponent = models.ForeignKey(
        User, related_name='opponent', null=True, blank=True, on_delete=models.DO_NOTHING)
    completed = models.DateTimeField(null=True, blank=True)
    creator_choice = models.TextField(null=True, blank=True,)
    opponent_choice = models.TextField(null=True, blank=True)
    status = models.TextField(blank=True, default="waiting")

    @staticmethod
    def get_available_games():
        return Game.objects.filter(status__exact="waiting").order_by('game_name')[:20]

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user) | Q(creator=user) & Q(status="completed"))

    @staticmethod
    def get_completed_games():
        return Game.objects.filter(status="completed").order_by('completed')

    @staticmethod
    def create_new(name, user):
        new_game = Game(creator=user, game_name=name)
        new_game.save()
        return new_game

    def mark_complete(self, winner):
        self.winner = winner
        self.completed = datetime.now()
        self.set_status("completed")
        self.save()

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


    @staticmethod
    def get_game(name):
        game = Game.objects.filter(game_name__exact=name)
        if game.exists():
            game = game.first()
        return game

    def __str__(self):
        return self.game_name

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
    def get_random():
        if Game.objects.filter(status__exact="waiting") is not None:
            return Game.objects.filter(status__exact="waiting").order_by("?").first()


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='player', on_delete=models.CASCADE)
    wins = models.IntegerField(blank=True, default=0)
    loses = models.IntegerField(blank=True, default=0)
    rating = models.FloatField(blank=True, default=0)


    @staticmethod
    def get_profile(user):
        profile = Profile.objects.filter(user=user)
        if profile.exists():
            profile = profile.first()
        else:
            profile = Profile.create_new_profile(user)
        return profile

    @staticmethod
    def create_new_profile(user):
        new_profile = Profile(user=user)
        new_profile.save()
        return new_profile

    def profile_wins(self):
        self.wins += 1
        self.save(update_fields=['wins'])
        self.wl()


    def profile_loses(self):
        self.loses += 1
        self.save(update_fields=['loses'])
        self.wl()


    def wl(self):
        if self.loses == 0:
            winlose = self.wins
        else:
            winlose = self.wins/self.loses
        self.rating = winlose
        self.save(update_fields=['rating'])

    @staticmethod
    def change_profile(user, kod):
        profile = Profile.get_profile(user)
        if kod==1:
            profile.profile_wins()
        else:
            profile.profile_loses()
