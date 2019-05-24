# chat/urls.py
from django.conf.urls import url
from django.views.generic import  ListView
from .models import Game
from . import views

urlpatterns = [
    #url(r'^$', ListView.as_view(queryset=Game.objects.filter(status__exact="waiting").order_by('game_name')[:20], template_name=views.index)),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

]