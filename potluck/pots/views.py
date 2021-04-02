from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from potluck.games.models import Game
from potluck.pots.models import Pot
from potluck.pots.forms import AddGameForm


class PotListView(generic.ListView):
    model = Pot
    context_object_name = "pots"


class PotDetailView(generic.DetailView):
    model = Pot
    context_object_name = "pot"


class PotCreateView(generic.CreateView):
    model = Pot
    success_url = reverse_lazy("pots:list")
    fields = ("name",)


class PotAddGameView(generic.CreateView):
    model = Game
    form_class = AddGameForm
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
        return reverse_lazy("pots:detail", kwargs={"pk": self.pot.id})
