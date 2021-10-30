import factory

from potluck.pots.models import Pot


class PotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pot

    name = factory.sequence(lambda n: f"test pot {n}")
