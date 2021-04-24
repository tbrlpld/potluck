import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.tests.factories import GamePickFactory, PickFactory


@pytest.mark.django_db
class TestPick:
    def setup(self):
        self.pick = PickFactory.create()
        self.game_1 = self.pick.pot.games.first()
        self.game_2 = self.pick.pot.games.last()

        self.game_1_winning_team = self.game_1.teams.first()
        self.game_1_loosing_team = self.game_1.teams.last()
        self.game_1.winning_team = self.game_1_winning_team

        self.game_2_winning_team = self.game_2.teams.first()
        self.game_2_loosing_team = self.game_2.teams.last()
        self.game_2.winning_team = self.game_2_winning_team

    def test_count_correct_game_picks_returns_0(self):
        GamePickFactory(
            pick=self.pick, game=self.game_1, picked_team=self.game_1_loosing_team
        )
        GamePickFactory(
            pick=self.pick, game=self.game_2, picked_team=self.game_2_loosing_team
        )

        result = self.pick.count_correct()

        assert result == 0


@pytest.mark.django_db
class TestGamePick:
    def test_is_correct_true_if_picked_team_matches_games_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        game.winning_team = winning_team
        game_pick = GamePickFactory(
            game=game,
            picked_team=winning_team
        )

        result = game_pick.is_correct()

        assert result is True

    def test_is_correct_false_if_picked_team_not_matches_games_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        loosing_team = game.teams.last()
        game.winning_team = winning_team
        game_pick = GamePickFactory(
            game=game,
            picked_team=loosing_team
        )

        result = game_pick.is_correct()

        assert result is False
