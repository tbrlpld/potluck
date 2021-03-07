# from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy


from potluck.games.forms import CreateGameForm
from potluck.games.models import Game


# Create your views here.
class CreateGameView(CreateView):
    model = Game
    form_class = CreateGameForm
    extra_context = {"title": "Create Game"}
    success_url = reverse_lazy("home:home")
