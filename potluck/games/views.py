from django.views import generic as gerneic_views
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from potluck.games.models import Game


class GameDeleteView(gerneic_views.DeleteView):
    model = Game
    context_object_name = "game"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.game = get_object_or_404(Game, pk=self.kwargs["pk"])
        self.pot = self.game.pot

    def get_success_url(self):
        return reverse_lazy("pots:detail", kwargs={"pk": self.pot.id})
