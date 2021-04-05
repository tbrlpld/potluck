import factory

from potluck.games.models import Game
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    pot = factory.SubFactory(PotFactory)

    @classmethod
    def create_with_teams(cls, **kwargs):
        game = cls(**kwargs)
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        game.teams.add(team_1)
        game.teams.add(team_2)
        game.save()
        return game
