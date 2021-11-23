from django import shortcuts, urls
from django.views import generic

from potluck.games import forms as games_forms
from potluck.games import models as games_models
from potluck.pots import models as pots_models


class CreateGame(generic.CreateView):
    model = games_models.Game
    form_class = games_forms.CreateGameInPotForm
    template_name = "pots/add_game.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot = shortcuts.get_object_or_404(
            pots_models.Pot, pk=self.kwargs["pot_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pot"] = self.pot
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pot"] = self.pot
        return kwargs

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})


class DeleteGame(generic.DeleteView):
    model = games_models.Game
    context_object_name = "game"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.game = shortcuts.get_object_or_404(games_models.Game, pk=self.kwargs["pk"])
        self.pot = self.game.pot

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})
