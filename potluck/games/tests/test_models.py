from django.core import exceptions

import pytest

from potluck.games import models as games_models
from potluck.games import factories as games_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestGame:
    @pytest.fixture
    def setup(self):
        self.game = games_factories.Game(with_teams=True)
        self.home_team = self.game.home_team
        self.away_team = self.game.away_team

    def test_get_teams(self, setup, django_assert_num_queries):
        with django_assert_num_queries(1):
            teams = self.game.get_teams()

            assert self.home_team in teams
            assert self.away_team in teams

    def test_set_winning_team_home(self, setup):
        self.game.set_winning_team(self.home_team)

        assert self.game.winning_team == self.home_team

    def test_set_and_save_winning_team_home(self, setup):
        self.game.set_and_save_winning_team(self.home_team)

        assert (
            games_models.Game.objects.get(pk=self.game.id).winning_team == self.home_team
        )

    # TODO: Test set winning team away

    def test_set_winning_team_with_team_not_in_game(self, setup):
        team_not_in_game = teams_factories.TeamFactory.create()
        assert team_not_in_game not in self.game.teams.all()

        self.game.set_winning_team(team_not_in_game)

        assert self.game.winning_team == team_not_in_game

    def test_set_and_save_winning_team_with_team_not_in_game(self, setup):
        team_not_in_game = teams_factories.TeamFactory.create()
        assert team_not_in_game != self.home_team
        assert team_not_in_game != self.away_team

        with pytest.raises(exceptions.ValidationError):
            self.game.set_and_save_winning_team(team_not_in_game)

    def test_set_winning_team_on_tie(self, setup):
        self.game.set_tie()
        assert self.game.is_tie is True

        self.game.set_winning_team(self.home_team)

        assert self.game.is_tie is False

    def test_is_tie(self):
        game = games_factories.Game(is_tie=True)

        assert game.is_tie is True

    def test_clean_with_is_tie_and_winning_team(self, setup):
        self.game.set_winning_team(self.home_team)
        self.game.is_tie = True

        with pytest.raises(exceptions.ValidationError):
            self.game.clean()

    def test_set_tie(self, setup):
        assert self.game.is_tie is not True

        self.game.set_tie()

        assert self.game.is_tie is True

    def test_set_tie_on_winning_team(self, setup):
        self.game.set_winning_team(self.home_team)
        assert self.game.winning_team == self.home_team
        assert self.game.is_tie is False

        self.game.set_tie()

        assert self.game.is_tie is True
        assert self.game.winning_team is None
