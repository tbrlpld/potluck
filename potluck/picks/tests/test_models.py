import pytest

from potluck.games.models import Game
from potluck.games import factories as games_factories
from potluck.picks.models import Pick, PickSheet
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory
from potluck.teams.models import Team
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestPickSheet:
    @pytest.fixture
    def setup_picksheet(self):
        self.pot = PotFactory.create()
        self.game_1 = games_factories.Game.create(pot=self.pot, with_teams=True)
        self.game_2 = games_factories.Game.create(pot=self.pot, with_teams=True)

        self.game_1_winning_team = self.game_1.away_team
        self.game_1_loosing_team = self.game_1.home_team
        self.game_1.winning_team = self.game_1_winning_team
        self.game_1.save()

        self.game_2_winning_team = self.game_2.home_team
        self.game_2_loosing_team = self.game_2.away_team
        self.game_2.winning_team = self.game_2_winning_team
        self.game_2.save()

        self.pick_sheet = PickSheetFactory.create(pot=self.pot)

    @pytest.fixture
    def place_game_1_wrong_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_loosing_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_1_correct_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_wrong_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_loosing_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_correct_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        yield pick

        pick.delete()

    def test_factory(self):
        pot = PotFactory.create()

        picksheet = PickSheetFactory.create(pot=pot)

        assert picksheet.pot == pot

    def test_basic_fields(self):
        pot = PotFactory.create()

        picksheet = PickSheetFactory.create(
            pot=pot,
            picker="Tester",
            tiebreaker_guess=13,
        )

        assert isinstance(picksheet.picker, str)
        assert picksheet.picker == "Tester"
        assert isinstance(picksheet.tiebreaker_guess, int)
        assert picksheet.tiebreaker_guess == 13

    def test_count_correct_method_returns_0_for_both_wrong(
        self,
        setup_picksheet,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 0

    def test_count_correct_method_returns_1_for_game_1_correct(
        self,
        setup_picksheet,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 1

    def test_count_correct_method_returns_1_for_game_2_correct(
        self,
        setup_picksheet,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 1

    def test_count_correct_method_returns_2_for_both_correct(
        self,
        setup_picksheet,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):

        result = self.pick_sheet.count_correct()

        assert result == 2

    def test_correct_count_annotation_returns_0_for_both_wrong(
        self,
        setup_picksheet,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(
            pk=self.pick_sheet.id
        )

        result = pick_sheet.correct_count

        assert result == 0

    def test_correct_count_annotation_returns_1_for_game_1_correct(
        self,
        setup_picksheet,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(
            pk=self.pick_sheet.id
        )

        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_1_for_game_2_correct(
        self,
        setup_picksheet,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(
            pk=self.pick_sheet.id
        )

        assert self.pick_sheet.count_correct() == 1
        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_2_for_both_correct(
        self,
        setup_picksheet,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(
            pk=self.pick_sheet.id
        )

        result = pick_sheet.correct_count

        assert result == 2

    def test_correct_count_annotation_still_works_when_other_pick_in_db(
        self,
        setup_picksheet,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        # Create another pick with 2 correct picks. It's existence can not influence the
        # fact that the pick under test only has one correct pick!
        other_pick_sheet = PickSheetFactory.create(
            pot=self.pot, picker="The Other Picker"
        )
        PickFactory.create(
            pick_sheet=other_pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        PickFactory.create(
            pick_sheet=other_pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )
        assert Pick.objects.count() == 4
        # Get the original pick, the one that is being tested
        pick_sheet = PickSheet.objects.annotate_correct_count().get(
            pk=self.pick_sheet.id
        )

        result = pick_sheet.correct_count

        assert result == 1

    @pytest.mark.parametrize(
        "score, guess, expected",
        [
            (20, 15, -5),
            (30, 10, -20),
            (30, 40, 10),
        ],
    )
    def test_tiebreaker_delta(self, score, guess, expected, django_assert_num_queries):
        pot = PotFactory.create(tiebreaker_score=score)
        pick_sheet = PickSheetFactory.create(pot=pot, tiebreaker_guess=guess)
        annotated_pick_sheets = PickSheet.objects.annotate_tiebreaker_delta().filter(
            pk=pick_sheet.id
        )

        with django_assert_num_queries(1):
            result = annotated_pick_sheets[0].tiebreaker_delta

        assert result == expected

    @pytest.mark.parametrize(
        "score, guess, expected",
        [
            (20, 15, 5),
            (30, 10, 20),
            (30, 40, 10),
        ],
    )
    def test_tiebreaker_delta_abs(
        self, score, guess, expected, django_assert_num_queries
    ):
        pot = PotFactory.create(tiebreaker_score=score)
        pick_sheet = PickSheetFactory.create(pot=pot, tiebreaker_guess=guess)
        annotated_pick_sheets = (
            PickSheet.objects.annotate_tiebreaker_delta_abs().filter(pk=pick_sheet.id)
        )

        with django_assert_num_queries(1):
            result = annotated_pick_sheets[0].tiebreaker_delta_abs

        assert result == expected


@pytest.mark.django_db
class TestPick:
    @pytest.fixture
    def setup_game_with_two_teams(self):
        self.game = games_factories.Game.create(with_teams=True)
        self.team_1 = self.game.away_team
        self.team_2 = self.game.home_team

    def test_is_correct_annotation_is_true_if_picked_team_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.team_1
        self.game.set_and_save_winning_team(winning_team)
        pick = PickFactory(game=self.game, picked_team=winning_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is True

    def test_is_correct_annotation_is_false_if_picked_team_not_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.team_1
        loosing_team = self.team_2
        self.game.set_and_save_winning_team(winning_team)
        pick = PickFactory(game=self.game, picked_team=loosing_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is False

    def test_is_correct_annotation_with_tied_game(self, setup_game_with_two_teams):
        self.game.set_tie()
        self.game.save()
        assert self.game.winning_team is None
        assert self.game.is_tie is True
        pick_team_1 = PickFactory(game=self.game, picked_team=self.team_1)
        pick_team_2 = PickFactory(game=self.game, picked_team=self.team_2)
        pick_team_1 = Pick.objects.annotate_is_correct().get(pk=pick_team_1.id)
        pick_team_2 = Pick.objects.annotate_is_correct().get(pk=pick_team_2.id)

        result_team_1 = pick_team_1.is_correct
        result_team_2 = pick_team_2.is_correct

        assert result_team_1 is False
        assert result_team_2 is False
