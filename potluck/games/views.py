from django import forms
from django import shortcuts
from django.urls import reverse_lazy
from django.views import generic as generic_views

from potluck.games.forms import GameAddForm, SetWinningTeamForm
from potluck.games.models import Game
from potluck.pots.models import Pot


class GameAddView(generic_views.CreateView):
    model = Game
    form_class = GameAddForm
    template_name = "pots/game_add.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot = shortcuts.get_object_or_404(Pot, pk=self.kwargs["pot_id"])

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
        self.game = shortcuts.get_object_or_404(Game, pk=self.kwargs["pk"])
        self.pot = self.game.pot

    def get_success_url(self):
        return reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})


class SetWinningTeamsView(generic_views.FormView):
    template_name = "games/set_winners.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(Pot, pk=self.pot_id)

    def get_form_class(self):
        return forms.modelformset_factory(
            Game,
            form=SetWinningTeamForm,
            max_num=self.pot.games.count(),
            min_num=self.pot.games.count(),
            validate_max=True,
            validate_min=True,
            extra=0,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"queryset": self.pot.games.all()})
        return kwargs

    def form_valid(self, forms):
        for form in forms:
            form.save()
        return shortcuts.redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("pot_detail", kwargs={"pk": self.pot_id})
