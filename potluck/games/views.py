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


def set_winning_teams(request, pot_id):
    pot = shortcuts.get_object_or_404(Pot, pk=pot_id)
    formset_games = pot.games.all()
    SetWinningTeamFormset = forms.modelformset_factory(
        Game,
        form=SetWinningTeamForm,
        max_num=pot.games.count(),
        min_num=pot.games.count(),
        validate_max=True,
        validate_min=True,
        extra=0,
    )
    if request.method == "POST":
        formset = SetWinningTeamFormset(request.POST, queryset=formset_games)
        if formset.is_valid():
            for form in formset:
                form.save()
            return shortcuts.redirect(
                reverse_lazy("pot_detail", kwargs={"pk": pot.id})
            )
    else:
        formset = SetWinningTeamFormset(queryset=formset_games)

    return shortcuts.render(
        request,
        template_name="games/set_winners.html",
        context={
            "formset": formset,
        },
    )
