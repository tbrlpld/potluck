import pytest

from potluck.picks.tests.factories import GamePickFactory, PickFactory
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPot:
    def test_tally_lists_picks_by_decending_number_of_correct_picks(self):
        pot = PotFactory.create()

        game_1 = pot.games.first()
        game_1_winning_team = game_1.teams.first()
        game_1_loosing_team = game_1.teams.last()
        game_1.winning_team = game_1_winning_team
        game_1.save()

        game_2 = pot.games.first()
        game_2_winning_team = game_2.teams.first()
        game_2_loosing_team = game_2.teams.last()
        game_2.winning_team = game_2_winning_team
        game_2.save()

        # Pick 1 with 1 correct game pick
        pick_1 = PickFactory(pot=pot)
        GamePickFactory(
            pick=pick_1, game=game_1, picked_team=game_1_winning_team
        )
        GamePickFactory(
            pick=pick_1, game=game_2, picked_team=game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        pick_2 = PickFactory(pot=pot)
        GamePickFactory(
            pick=pick_2, game=game_1, picked_team=game_1_winning_team
        )
        GamePickFactory(
            pick=pick_2, game=game_2, picked_team=game_2_winning_team
        )

        result = pot.get_tally()

        assert result[0] == pick_2
        assert result[1] == pick_1