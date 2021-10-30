import factory

from potluck.games.models import Game


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
