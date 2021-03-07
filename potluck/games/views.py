# from django.shortcuts import render
from django.views.generic import CreateView


from potluck.games.models import Game


# Create your views here.
class CreateGameView(CreateView):
    model = Game
    fields = ("teams",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Game"
        return context
