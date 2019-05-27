# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from rps.models import Profile, Game


@login_required(login_url='/login/')
def room(request, room_name):
    return render(request, 'rps/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
@login_required(login_url='/login/')
def mygames (request):
    return render(request, 'rps/mygames.html',{
        'games_for_player': Game.get_games_for_player(request.user)[:20],
        'profile': Profile.objects.filter(user=request.user).first()
    })



@login_required(login_url='/login/')
def statistic(request):
    return render(request,'rps/statistic.html',{
       'best_player': Profile.objects.all().order_by("-rating").first(),
        'worst_player': Profile.objects.all().order_by("rating").first(),
        'available_games': Game.objects.filter(status="waiting").count(),
        'completed_games': Game.objects.filter(status="completed").count(),
        'completed_games_list': Game.objects.filter(status="completed"),
    })


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'rps/register.html'



