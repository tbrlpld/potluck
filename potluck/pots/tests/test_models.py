import pytest

from potluck.games import factories as games_factories
from potluck.picks.tests import factories as picks_factories
from potluck.pots import models as pots_models
from potluck.pots.tests import factories as pots_factories


@pytest.mark.django_db
class TestPot:
    @pytest.fixture
    def setup_pot_with_two_games(self):

        self.pot = pots_factories.PotFactory.create()

        self.game_1 = games_factories.Game.create(pot=self.pot, with_teams=True)
        self.team_1 = self.game_1.home_team
        self.team_2 = self.game_1.away_team
        self.game_1_winning_team = self.team_1
        self.game_1_loosing_team = self.team_2
        self.game_1.set_and_save_winning_team(self.game_1_winning_team)

        self.game_2 = games_factories.Game.create(pot=self.pot, with_teams=True)
        self.team_3 = self.game_2.away_team
        self.team_4 = self.game_2.home_team
        self.game_2_winning_team = self.team_3
        self.game_2_loosing_team = self.team_4
        self.game_2.set_and_save_winning_team(self.game_2_winning_team)

    def test_factory(self):
        pots_factories.PotFactory.create()

        assert True

    def test_pot_fields(self):
        pot = pots_factories.PotFactory.create(name="Test Pot", tiebreaker_score=13)

        assert isinstance(pot.name, str)
        assert pot.name == "Test Pot"
        assert isinstance(pot.tiebreaker_score, int)
        assert pot.tiebreaker_score == 13

    def test_tally_lists_picks_by_decending_number_of_correct_picks(
        self,
        setup_pot_with_two_games,
    ):
        # Pick with 1 correct game pick
        pick_sheet_1 = picks_factories.PickSheetFactory.create(pot=self.pot)
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_1,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_1,
            game=self.game_2,
            picked_team=self.game_2_loosing_team,
        )

        # Pick with 0 correct game pick
        pick_sheet_0 = picks_factories.PickSheetFactory.create(pot=self.pot)
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_0,
            game=self.game_1,
            picked_team=self.game_1_loosing_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_0,
            game=self.game_2,
            picked_team=self.game_2_loosing_team,
        )

        # Pick with 2 correct game picks
        pick_sheet_2 = picks_factories.PickSheetFactory.create(pot=self.pot)
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        result = self.pot.get_tally()

        assert result[0] == pick_sheet_2
        assert result[1] == pick_sheet_1
        assert result[2] == pick_sheet_0

    def test_tally_with_tie(
        self,
        setup_pot_with_two_games,
    ):
        tiebreaker_score = 50
        self.pot.tiebreaker_score = tiebreaker_score
        self.pot.save()

        # Pick with 2 correct game picks, 20 off tiebreaker
        pick_sheet_2_20 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score - 20,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_20,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_20,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        # Pick with 1 correct game pick, and exact tiebreaker score.
        # The tiebreaker score of this pick sheet does not matter because the
        # correct number of games is not the highest.
        pick_sheet_1_0 = picks_factories.PickSheetFactory.create(
            pot=self.pot, tiebreaker_guess=60
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_1_0,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_1_0,
            game=self.game_2,
            picked_team=self.game_2_loosing_team,
        )

        # Pick with 2 correct game picks, 10 off tiebreaker
        pick_sheet_2_10 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score - 10,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_10,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_10,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        result = self.pot.get_tally()

        assert result[0] == pick_sheet_2_10
        assert result[1] == pick_sheet_2_20
        assert result[2] == pick_sheet_1_0

    def test_tally_with_tiebreaker_guess_larger_than_score_winning(
        self,
        setup_pot_with_two_games,
    ):
        tiebreaker_score = 50
        self.pot.tiebreaker_score = tiebreaker_score
        self.pot.save()

        pick_sheet_2_minus_10 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score - 10,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_minus_10,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_minus_10,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        pick_sheet_2_plus_5 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score + 5,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_plus_5,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_plus_5,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        result = self.pot.get_tally()

        assert result[0] == pick_sheet_2_plus_5
        assert result[1] == pick_sheet_2_minus_10

    def test_tally_with_tiebreaker_guess_larger_than_score_losing(
        self,
        setup_pot_with_two_games,
    ):
        tiebreaker_score = 50
        self.pot.tiebreaker_score = tiebreaker_score
        self.pot.save()

        pick_sheet_2_plus_10 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score + 10,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_plus_10,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_plus_10,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        pick_sheet_2_minus_5 = picks_factories.PickSheetFactory.create(
            pot=self.pot,
            tiebreaker_guess=tiebreaker_score - 5,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_minus_5,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory.create(
            pick_sheet=pick_sheet_2_minus_5,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        result = self.pot.get_tally()

        assert result[0] == pick_sheet_2_minus_5
        assert result[1] == pick_sheet_2_plus_10

    @pytest.mark.parametrize(
        "initial_status, expected_next_status",
        [
            (pots_models.Pot.Status.DRAFT, pots_models.Pot.Status.OPEN),
            (pots_models.Pot.Status.OPEN, pots_models.Pot.Status.CLOSED),
            (pots_models.Pot.Status.CLOSED, pots_models.Pot.Status.TALLY),
            (pots_models.Pot.Status.TALLY, None),
        ],
    )
    def test_next_status(self, initial_status, expected_next_status):
        pot = pots_factories.PotFactory.create(status=initial_status)

        next_status = pot.next_status

        assert next_status == expected_next_status

    @pytest.mark.parametrize(
        "initial_status, expected_previous_status",
        [
            (pots_models.Pot.Status.DRAFT, None),
            (pots_models.Pot.Status.OPEN, pots_models.Pot.Status.DRAFT),
            (pots_models.Pot.Status.CLOSED, pots_models.Pot.Status.OPEN),
            (pots_models.Pot.Status.TALLY, pots_models.Pot.Status.CLOSED),
        ],
    )
    def test_previous_status(self, initial_status, expected_previous_status):
        pot = pots_factories.PotFactory.create(status=initial_status)

        previous_status = pot.previous_status

        assert previous_status == expected_previous_status
