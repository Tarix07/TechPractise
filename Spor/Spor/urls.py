# mysite/urls.py
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import ListView
from rps.models import Game
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from rps import forms, views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    url(r'^game/', include('rps.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(ListView.as_view(queryset=Game.get_available_games(),
            template_name='rps/index.html'), login_url='/login/'), name='home'),
    url(r'^mygames/', views.mygames, name='mygames'),
    url(r'^statistic/', views.statistic, name='statistic'),
   ]