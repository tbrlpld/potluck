import factory

from potluck.games.models import Game
from potluck.teams.tests.factories import TeamFactory


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        # If not called with the create method, do nothing.
        if not create:
            return

        # If a list was passed into the create method, use that
        if extracted:
            for team in extracted:
                self.teams.add(team)
        # If noting was passed, create and add two teams to the game.
        else:
            self.teams.add(TeamFactory.create())
            self.teams.add(TeamFactory.create())
