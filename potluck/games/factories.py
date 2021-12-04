import factory

from potluck.games.models import Game


class Game(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    class Params:
        with_teams = factory.Trait()
