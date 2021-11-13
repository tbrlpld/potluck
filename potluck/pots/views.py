from django import forms, shortcuts, urls
from django.views import generic

from potluck.games.models import Game
from potluck.games.forms import SetWinningTeamForm
from potluck.picks.models import PickSheet
from potluck.pots.forms import CreateGameInPotForm, SetTiebreakerScoreForm
from potluck.pots.models import Pot


class PotListView(generic.ListView):
    model = Pot
    context_object_name = "pots"
    ordering = "-id"


class PotDetailView(generic.DetailView):
    model = Pot
    context_object_name = "pot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        picks_url = urls.reverse_lazy("pick_create", kwargs={"pot_id": self.object.id})
        context["picks_url"] = self.request.build_absolute_uri(picks_url)

        return context


class PotCreateView(generic.CreateView):
    model = Pot
    template_name = "pots/pot_create.html"
    success_url = urls.reverse_lazy("pots_list")
    fields = ("name",)


class PotDeleteView(generic.DeleteView):
    model = Pot
    template_name = "pots/pot_delete.html"
    success_url = urls.reverse_lazy("pots_list")


class UpdatePotStatusView(generic.UpdateView):
    model = Pot
    fields = ("status",)
    http_method_names = ["post"]

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.kwargs["pk"]})


class AddGameView(generic.CreateView):
    model = Game
    form_class = CreateGameInPotForm
    template_name = "pots/add_game.html"

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
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})


class TallyView(generic.ListView):
    template_name = "pots/tally.html"
    model = PickSheet
    context_object_name = "picks"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(Pot, pk=self.pot_id)

    def get_queryset(self):
        return self.pot.get_tally()

    def get_context_data(self):
        context = super().get_context_data()
        context["pot"] = self.pot
        return context


def set_results(request, pot_id):
    pot = shortcuts.get_object_or_404(Pot, pk=pot_id)
    games_queryset = pot.games.all().order_by("id")
    winning_teams_prefix = "winning-teams"
    SetWinningTeamsFormset = forms.modelformset_factory(
        Game,
        form=SetWinningTeamForm,
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
        set_tiebreaker_score_form = SetTiebreakerScoreForm(
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
        set_tiebreaker_score_form = SetTiebreakerScoreForm(instance=pot)
    return shortcuts.render(
        request,
        template_name="pots/set_results.html",
        context={
            "pot": pot,
            "set_winning_teams_formset": set_winning_teams_formset,
            "set_tiebreaker_score_form": set_tiebreaker_score_form,
        },
    )
