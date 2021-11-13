import factory
from factory import fuzzy

from potluck.pots.models import Pot


class PotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pot

    name = factory.sequence(lambda n: f"test pot {n}")
    tiebreaker_score = fuzzy.FuzzyInteger(1, 100)
