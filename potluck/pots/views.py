from django.urls import reverse_lazy
from django.views import generic

from potluck.pots.models import Pot


class PotListView(generic.ListView):
    model = Pot
    context_object_name = "pots"


class PotDetailView(generic.DetailView):
    model = Pot
    context_object_name = "pot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        picks_url = reverse_lazy("pick_create", kwargs={"pot_id": self.object.id })
        context["picks_url"] = self.request.build_absolute_uri(picks_url)

        return context


class PotCreateView(generic.CreateView):
    model = Pot
    success_url = reverse_lazy("pots_list")
    fields = ("name",)
