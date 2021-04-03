from django import shortcuts
from django.views import generic as generic_views

from potluck.games.models import Game
from potluck.picks.models import GamePick
from potluck.picks.forms import CreateGamePickForm


class CreateGamePickView(generic_views.CreateView):
    model = GamePick
    form_class = CreateGamePickForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        game_id = self.kwargs.get("game_id")
        self.game = shortcuts.get_object_or_404(Game, pk=game_id)

    def get_initial(self):
        initial = super().get_initial()
        initial["game"] = self.game
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game"] = self.game
        return context
