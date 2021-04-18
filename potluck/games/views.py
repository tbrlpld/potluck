from django import shortcuts
from django.urls import reverse_lazy
from django.views import generic as generic_views

from potluck.games.models import Game


class GameDeleteView(generic_views.DeleteView):
    model = Game
    context_object_name = "game"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.game = shortcuts.get_object_or_404(Game, pk=self.kwargs["pk"])
        self.pot = self.game.pot

    def get_success_url(self):
        return reverse_lazy("pot_detail", kwargs={"pk": self.pot.id})
