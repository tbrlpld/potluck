import factory

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import GamePick


class GamePickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GamePick

    game = factory.SubFactory(GameFactory)
