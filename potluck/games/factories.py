import factory

from potluck.games.models import Game
from potluck.teams.tests import factories as teams_factories


class Game(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    class Params:
        with_teams = factory.Trait(
            home_team=factory.SubFactory(teams_factories.TeamFactory),
            away_team=factory.SubFactory(teams_factories.TeamFactory),
        )
