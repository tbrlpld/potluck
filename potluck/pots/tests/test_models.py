import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestPot:
    @pytest.fixture
    def setup_pot_with_two_games(self):
        self.team_1 = TeamFactory.create()
        self.team_2 = TeamFactory.create()
        self.team_3 = TeamFactory.create()
        self.team_4 = TeamFactory.create()

        self.pot = PotFactory.create()

        self.game_1 = GameFactory.create(pot=self.pot)
        self.game_1.teams.set((self.team_1, self.team_2))
        self.game_1_winning_team = self.team_1
        self.game_1_loosing_team = self.team_2
        self.game_1.set_winning_team(self.game_1_winning_team)

        self.game_2 = GameFactory.create(pot=self.pot)
        self.game_2.teams.set((self.team_3, self.team_4))
        self.game_2_winning_team = self.team_3
        self.game_2_loosing_team = self.team_4
        self.game_2.set_winning_team(self.game_2_winning_team)

    def test_tally_lists_picks_by_decending_number_of_correct_picks(
        self,
        setup_pot_with_two_games,
    ):
        # Pick 1 with 1 correct game pick
        pick_sheet_1 = PickSheetFactory.create(pot=self.pot)
        PickFactory.create(
            pick_sheet=pick_sheet_1,
            game=self.game_1,
            picked_team=self.game_1_winning_team
        )
        PickFactory.create(
            pick_sheet=pick_sheet_1,
            game=self.game_2,
            picked_team=self.game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        pick_sheet_2 = PickSheetFactory.create(pot=self.pot)
        PickFactory.create(
            pick_sheet=pick_sheet_2,
            game=self.game_1,
            picked_team=self.game_1_winning_team
        )
        PickFactory.create(
            pick_sheet=pick_sheet_2,
            game=self.game_2,
            picked_team=self.game_2_winning_team
        )

        result = self.pot.get_tally()

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
