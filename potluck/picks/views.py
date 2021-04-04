from django import shortcuts
from django import urls
from django.views import generic as generic_views

from potluck.games.models import Game
from potluck.picks.models import GamePick, Pick
from potluck.picks.forms import GamePickFormset, CreatePickForm
from potluck.picks.models import Pot


class CreatePickView(generic_views.CreateView):
    form_class = CreatePickForm
    template_name = "picks/create.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(Pot, pk=self.pot_id)

    def get_initial(self):
        initial = super().get_initial()
        initial["pot"] = self.pot
        return initial

    def get_success_url(self):
        return urls.reverse_lazy(
            "games_pick",
            kwargs={"pot_id": self.pot_id, "pick_id": self.object.id},
        )


class AddGamePicksView(generic_views.FormView):
    form_class = GamePickFormset
    template_name = "picks/add_games.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(Pot, pk=self.pot_id)
        self.pick_id = kwargs.get("pick_id")
        self.pick = shortcuts.get_object_or_404(Pick, pk=self.pick_id)

    def get_initial(self):
        initial = []
        for game in self.pot.games.all():
            initial.append(
                {
                    "game": game,
                    "pick": self.pick,
                }
            )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pot"] = self.pot
        return context

    def form_valid(self, formset):
        for form in formset:
            form.save()
        return super().form_valid(formset)

    def get_success_url(self):
        return urls.reverse_lazy("pots_list")
