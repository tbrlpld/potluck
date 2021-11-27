from django import forms, shortcuts, urls
from django.views import generic

from potluck.games import forms as games_forms
from potluck.games import models as games_models
from potluck.pots import forms as pots_forms
from potluck.pots import models as pots_models


class CreateGame(generic.CreateView):
    model = games_models.Game
    form_class = games_forms.CreateGame
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


def set_results(request, pot_id):
    pot = shortcuts.get_object_or_404(pots_models.Pot, pk=pot_id)
    games_queryset = pot.games.all().order_by("id")
    winning_teams_prefix = "winning-teams"
    SetGameResultFormset = forms.formset_factory(
        form=games_forms.SetGameResult,
        formset=games_forms.BaseSetGameResultFormSet,
        max_num=pot.games.count(),
        min_num=pot.games.count(),
        validate_max=True,
        validate_min=True,
        extra=0,
    )

    if request.method == "POST":
        set_game_result_formset = SetGameResultFormset(
            data=request.POST,
            games=games_queryset,
            prefix=winning_teams_prefix,
        )
        set_tiebreaker_score_form = pots_forms.SetTiebreakerScore(
            data=request.POST, instance=pot
        )
        if all(
            (set_game_result_formset.is_valid(), set_tiebreaker_score_form.is_valid())
        ):
            for set_game_result_form in set_game_result_formset:
                set_game_result_form.save()
            set_tiebreaker_score_form.save()
            return shortcuts.redirect(
                urls.reverse_lazy("pot_detail", kwargs={"pk": pot_id})
            )
    else:
        set_game_result_formset = SetGameResultFormset(
            games=games_queryset,
            prefix=winning_teams_prefix,
        )
        set_tiebreaker_score_form = pots_forms.SetTiebreakerScore(instance=pot)

    return shortcuts.render(
        request,
        template_name="games/set_results.html",
        context={
            "pot": pot,
            "set_game_result_formset": set_game_result_formset,
            "set_tiebreaker_score_form": set_tiebreaker_score_form,
        },
    )
