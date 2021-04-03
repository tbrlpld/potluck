from django import shortcuts
from django.views import generic as generic_views

from potluck.games.models import Game
from potluck.picks.models import GamePick
from potluck.picks.forms import CreateGamePickForm, GamePickFormset
from potluck.picks.models import Pot


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


class CreatePickView(generic_views.FormView):
    form_class = GamePickFormset
    template_name = "picks/pick_formset.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request)
        self.pot = Pot.objects.first()

    def get_initial(self):
        initial = []
        for game in self.pot.games.all():
            initial.append({"game": game})
        return initial
