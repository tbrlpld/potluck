import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestPot:
    def test_tally_lists_picks_by_decending_number_of_correct_picks(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        team_3 = TeamFactory.create()
        team_4 = TeamFactory.create()

        pot = PotFactory.create()

        game_1 = GameFactory.create(pot=pot)
        game_1.teams.set((team_1, team_2))
        game_1_winning_team = team_1
        game_1.set_winning_team(game_1_winning_team)

        game_2 = GameFactory.create(pot=pot)
        game_2.teams.set((team_3, team_4))
        game_2_winning_team = team_3
        game_2_loosing_team = team_4
        game_2.set_winning_team(game_2_winning_team)

        # Pick 1 with 1 correct game pick
        pick_sheet_1 = PickSheetFactory.create(pot=pot)
        PickFactory.create(
            pick_sheet=pick_sheet_1, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory.create(
            pick_sheet=pick_sheet_1, game=game_2, picked_team=game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        pick_sheet_2 = PickSheetFactory.create(pot=pot)
        PickFactory.create(
            pick_sheet=pick_sheet_2, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory.create(
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
        ],
    )
    def test_next_status(self, initial_status, expected_next_status):
        pot = PotFactory.create(status=initial_status)

        next_status = pot.next_status

        assert next_status == expected_next_status

    @pytest.mark.parametrize(
        "initial_status, expected_previous_status",
        [
            (Pot.Status.DRAFT, None),
            (Pot.Status.OPEN, Pot.Status.DRAFT),
            (Pot.Status.CLOSED, Pot.Status.OPEN),
            (Pot.Status.TALLY, Pot.Status.CLOSED),
        ],
    )
    def test_previous_status(self, initial_status, expected_previous_status):
        pot = PotFactory.create(status=initial_status)

        previous_status = pot.previous_status

        assert previous_status == expected_previous_status
