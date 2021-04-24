import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.tests.factories import GamePickFactory


@pytest.mark.django_db
class TestGamePick:
    def test_is_correct_true_if_picket_team_matches_games_winning_team(self):
        game = GameFactory.create_with_teams()
        winning_team = game.teams.first()
        loosing_team = game.teams.last()
        game.winning_team = winning_team
        game_pick = GamePickFactory(
            game=game,
            picked_team=winning_team
        )

        result = game_pick.is_correct()

        assert result is True
