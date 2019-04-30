from django.contrib.auth.models import User
from  django.db import models


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


