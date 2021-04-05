from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as generic_views

from potluck.games.forms import GameAddForm
from potluck.games.models import Game, Pot


class GameAddView(generic_views.CreateView):
    model = Game
    form_class = GameAddForm
    template_name = "pots/game_add.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot = get_object_or_404(Pot, pk=self.kwargs["pot_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pot"] = self.pot
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["pot"] = self.kwargs["pot_id"]
        return initial

    def get_success_url(self):
        return reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})


class GameDeleteView(generic_views.DeleteView):
    model = Game
    context_object_name = "game"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.game = get_object_or_404(Game, pk=self.kwargs["pk"])
        self.pot = self.game.pot

    def get_success_url(self):
        return reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})
