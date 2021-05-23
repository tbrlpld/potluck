import factory

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import GamePickTemp, Pick
from potluck.pots.tests.factories import PotFactory


class PickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pick

    picker = factory.Faker("first_name")
    pot = factory.SubFactory(PotFactory)


class GamePickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GamePickTemp

    pick = factory.SubFactory(PickFactory)
    game = factory.SubFactory(GameFactory)
