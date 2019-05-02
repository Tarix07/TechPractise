from builtins import staticmethod
from django.contrib.auth.models import User
from django.db import models


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


