from django import forms, shortcuts, urls
from django.views import generic

from potluck.games.models import Game
from potluck.picks.models import PickSheet
from potluck.pots.forms import GameAddForm, SetWinningTeamForm
from potluck.pots.models import Pot


class PotListView(generic.ListView):
    model = Pot
    context_object_name = "pots"


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


class UpdatePotStatusView(generic.UpdateView):
    model = Pot
    fields = ("status",)
    http_method_names = ["post"]

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.kwargs["pk"]})


class AddGameView(generic.CreateView):
    model = Game
    form_class = GameAddForm
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


class SetWinningTeamsView(generic.FormView):
    template_name = "pots/set_winning_teams.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pot"] = self.pot
        return context

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.pot_id})


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
