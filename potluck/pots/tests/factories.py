import factory

from potluck.games.tests.factories import GameFactory
from potluck.pots.models import Pot


class PotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pot

    name = factory.Sequence(lambda n: f"Test Pot {n}")

    @factory.post_generation
    def games(self, create, extracted, **kwargs):
        # If not called with the create method, do nothing.
        if not create:
            return

        # If a list was passed into the create method, use that
        if extracted:
            for game in extracted:
                game.pot = self
                game.save()
        # If noting was passed, create and add two teams to the game.
        else:
            GameFactory.create(pot=self)
            GameFactory.create(pot=self)

    @classmethod
    def create_without_games(cls):
        obj = cls.build()
        obj.save()
        return obj
