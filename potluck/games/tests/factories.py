import factory

from potluck.games.models import Game
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

