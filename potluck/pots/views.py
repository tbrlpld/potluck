from django.views import generic

from potluck.pots.models import Pot


class PotListView(generic.ListView):
    model = Pot
