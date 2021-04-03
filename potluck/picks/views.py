from django import shortcuts
from django import urls
from django.views import generic as generic_views

from potluck.games.models import Game
from potluck.picks.models import GamePick
from potluck.picks.forms import GamePickFormset, CreatePickForm
from potluck.picks.models import Pot


class CreatePickView(generic_views.CreateView):
    form_class = CreatePickForm
    template_name = "picks/create.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request)
        self.pot = Pot.objects.first()

    def get_initial(self):
        initial = super().get_initial()
        initial["pot"] = self.pot
        return initial

    def get_success_url(self):
        return urls.reverse_lazy("picks:pick_games")


class AddGamePicksView(generic_views.FormView):
    form_class = GamePickFormset
    template_name = "picks/add_games.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request)
        self.pot = Pot.objects.first()

    def get_initial(self):
        initial = []
        for game in self.pot.games.all():
            initial.append({"game": game})
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context["pot"] = self.pot
        return context

    def form_valid(self, formset):
        for form in formset:
            form.save()
        return super().form_valid(formset)

    def get_success_url(self):
        return urls.reverse_lazy("pots:list")
