from django import forms, shortcuts, urls
from django.views import generic

from potluck.games import forms as games_forms
from potluck.games import models as games_models
from potluck.picks import models as picks_models
from potluck.pots import forms as pots_forms
from potluck.pots import models as pots_models


class PotListView(generic.ListView):
    model = pots_models.Pot
    context_object_name = "pots"
    ordering = "-id"


class PotDetailView(generic.DetailView):
    model = pots_models.Pot
    context_object_name = "pot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        picks_url = urls.reverse_lazy("pick_create", kwargs={"pot_id": self.object.id})
        context["picks_url"] = self.request.build_absolute_uri(picks_url)

        return context


class PotCreateView(generic.CreateView):
    model = pots_models.Pot
    template_name = "pots/pot_create.html"
    success_url = urls.reverse_lazy("pots_list")
    fields = ("name", "tiebreaker_description")


class PotDeleteView(generic.DeleteView):
    model = pots_models.Pot
    template_name = "pots/pot_delete.html"
    success_url = urls.reverse_lazy("pots_list")


class UpdatePotStatusView(generic.UpdateView):
    model = pots_models.Pot
    fields = ("status",)
    http_method_names = ["post"]

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.kwargs["pk"]})


class TallyView(generic.ListView):
    template_name = "pots/tally.html"
    model = picks_models.PickSheet
    context_object_name = "pick_sheets"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(pots_models.Pot, pk=self.pot_id)

    def get_queryset(self):
        return self.pot.get_tally()

    def get_context_data(self):
        context = super().get_context_data()
        context["pot"] = self.pot
        return context


def set_results(request, pot_id):
    pot = shortcuts.get_object_or_404(pots_models.Pot, pk=pot_id)
    games_queryset = pot.games.all().order_by("id")
    winning_teams_prefix = "winning-teams"
    SetWinningTeamsFormset = forms.modelformset_factory(
        games_models.Game,
        form=games_forms.SetWinningTeamForm,
        max_num=pot.games.count(),
        min_num=pot.games.count(),
        validate_max=True,
        validate_min=True,
        extra=0,
    )
    if request.method == "POST":
        set_winning_teams_formset = SetWinningTeamsFormset(
            data=request.POST,
            queryset=games_queryset,
            prefix=winning_teams_prefix,
        )
        set_tiebreaker_score_form = pots_forms.SetTiebreakerScoreForm(
            data=request.POST, instance=pot
        )
        if all(
            (set_winning_teams_formset.is_valid(), set_tiebreaker_score_form.is_valid())
        ):
            set_winning_teams_formset.save()
            set_tiebreaker_score_form.save()
            return shortcuts.redirect(
                urls.reverse_lazy("pot_detail", kwargs={"pk": pot_id})
            )
    else:
        set_winning_teams_formset = SetWinningTeamsFormset(
            queryset=games_queryset,
            prefix=winning_teams_prefix,
        )
        set_tiebreaker_score_form = pots_forms.SetTiebreakerScoreForm(instance=pot)
    return shortcuts.render(
        request,
        template_name="pots/set_results.html",
        context={
            "pot": pot,
            "set_winning_teams_formset": set_winning_teams_formset,
            "set_tiebreaker_score_form": set_tiebreaker_score_form,
        },
    )
