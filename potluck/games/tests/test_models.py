from django.core import exceptions

import pytest

from potluck.games import models as games_models
from potluck.games.tests import factories as games_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestGame:
    @pytest.fixture
    def setup(self):
        self.team_1 = teams_factories.TeamFactory.create()
        self.team_2 = teams_factories.TeamFactory.create()
        self.game = games_factories.GameFactory.create()
        self.game.teams.set((self.team_1, self.team_2))

    def test_set_winning_team_saves_to_db(self, setup):
        self.game.set_winning_team(self.team_1)

        assert (
            games_models.Game.objects.get(pk=self.game.id).winning_team == self.team_1
        )

    def test_set_winning_team_with_team_not_in_game(self, setup):
        team_not_in_game = teams_factories.TeamFactory.create()
        assert team_not_in_game not in self.game.teams.all()

        with pytest.raises(exceptions.ValidationError):
            self.game.set_winning_team(team_not_in_game)

    def test_is_tie(self):
        game = games_factories.GameFactory(is_tie=True)

        assert game.is_tie == True
