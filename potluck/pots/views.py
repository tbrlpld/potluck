from django.urls import reverse_lazy
from django.views import generic

from potluck.pots.models import Pot


class PotListView(generic.ListView):
    model = Pot
    context_object_name = "pots"


class PotDetailView(generic.DetailView):
    model = Pot
    context_object_name = "pot"


class PotCreateView(generic.CreateView):
    model = Pot
    success_url = reverse_lazy("pots:list")
    fields = ("name",)
