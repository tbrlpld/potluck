import factory

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import Pick, PickSheet
from potluck.pots.tests.factories import PotFactory


class PickSheetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PickSheet

    picker = factory.Faker("first_name")
    pot = factory.SubFactory(PotFactory)


class PickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pick

    pick_sheet = factory.SubFactory(PickSheetFactory)
    game = factory.SubFactory(GameFactory)
