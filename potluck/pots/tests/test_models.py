import pytest

from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory



@pytest.mark.django_db
class TestPot:
    def test_tally_lists_picks_by_decending_number_of_correct_picks(self):
        pot = PotFactory.create()
        #
        game_1 = pot.games.first()
        game_1_winning_team = game_1.teams.first()
        game_1_loosing_team = game_1.teams.last()
        game_1.set_winning_team(game_1_winning_team)
        #
        game_2 = pot.games.first()
        game_2_winning_team = game_2.teams.first()
        game_2_loosing_team = game_2.teams.last()
        game_2.set_winning_team(game_2_winning_team)
        # Pick 1 with 1 correct game pick
        pick_sheet_1 = PickSheetFactory(pot=pot)
        PickFactory(
            pick_sheet=pick_sheet_1, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory(
            pick_sheet=pick_sheet_1, game=game_2, picked_team=game_2_loosing_team
        )
        # Pick 2 with 2 correct game picks
        pick_sheet_2 = PickSheetFactory(pot=pot)
        PickFactory(
            pick_sheet=pick_sheet_2, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory(
            pick_sheet=pick_sheet_2, game=game_2, picked_team=game_2_winning_team
        )

        result = pot.get_tally()

        assert result[0] == pick_sheet_2
        assert result[1] == pick_sheet_1


    @pytest.mark.parametrize(
        "initial_status, expected_next_status",
        [
            (Pot.Status.DRAFT, Pot.Status.OPEN),
            (Pot.Status.OPEN, Pot.Status.CLOSED),
            (Pot.Status.CLOSED, Pot.Status.TALLY),
            (Pot.Status.TALLY, None),
        ]
    )
    def test_next_status(self, initial_status, expected_next_status):
        pot = PotFactory.create(status=initial_status)

        next_status = pot.next_status

        assert next_status == expected_next_status
