from django.core import exceptions

import pytest

from potluck.games import models as games_models
from potluck.games.tests import factories as games_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestGame:
    @pytest.fixture
    def setup(self):
        pot = pots_factories.PotFactory()
        self.team_1 = teams_factories.TeamFactory()
        self.team_2 = teams_factories.TeamFactory()
        self.game = games_factories.GameFactory(pot=pot)
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

    def test_set_winning_team_on_tie(self, setup):
        self.game.set_tie()
        assert self.game.is_tie is True

        self.game.set_winning_team(self.team_1)

        assert self.game.is_tie is False

    def test_is_tie(self):
        game = games_factories.GameFactory(is_tie=True)

        assert game.is_tie is True

    def test_clean_with_is_tie_and_winning_team(self, setup):
        self.game.set_winning_team(self.team_1)
        self.game.is_tie = True

        with pytest.raises(exceptions.ValidationError):
            self.game.clean()

    def test_set_tie(self, setup):
        assert self.game.is_tie is not True

        self.game.set_tie()

        assert self.game.is_tie is True

    def test_set_tie_on_winning_team(self, setup):
        self.game.set_winning_team(self.team_1)
        assert self.game.winning_team == self.team_1
        assert self.game.is_tie is False

        self.game.set_tie()

        assert self.game.is_tie is True
        assert self.game.winning_team == None
