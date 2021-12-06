import pytest

from potluck.games import factories as games_factories
from potluck.picks import models as picks_models
from potluck.picks.tests import factories as picks_factories
from potluck.pots.tests import factories as pots_factories


@pytest.mark.django_db
class TestPickSheet:
    @pytest.fixture
    def setup_picksheet(self):
        self.pot = pots_factories.PotFactory()
        self.game_1 = games_factories.Game(pot=self.pot, with_teams=True)
        self.game_2 = games_factories.Game(pot=self.pot, with_teams=True)

        self.game_1_winning_team = self.game_1.away_team
        self.game_1_loosing_team = self.game_1.home_team
        self.game_1.winning_team = self.game_1_winning_team
        self.game_1.save()

        self.game_2_winning_team = self.game_2.home_team
        self.game_2_loosing_team = self.game_2.away_team
        self.game_2.winning_team = self.game_2_winning_team
        self.game_2.save()

        self.pick_sheet = picks_factories.PickSheetFactory(pot=self.pot)

    @pytest.fixture
    def place_game_1_wrong_pick(self):
        pick = picks_factories.PickFactory(
            pick_sheet=self.pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_loosing_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_1_correct_pick(self):
        pick = picks_factories.PickFactory(
            pick_sheet=self.pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_wrong_pick(self):
        pick = picks_factories.PickFactory(
            pick_sheet=self.pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_loosing_team,
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_correct_pick(self):
        pick = picks_factories.PickFactory(
            pick_sheet=self.pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )

        yield pick

        pick.delete()

    def test_factory(self):
        pot = pots_factories.PotFactory()

        picksheet = picks_factories.PickSheetFactory(pot=pot)

        assert picksheet.pot == pot

    def test_basic_fields(self):
        pot = pots_factories.PotFactory()

        picksheet = picks_factories.PickSheetFactory(
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
        pick_sheet =picks_models.PickSheet.objects.annotate_correct_count().get(
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
        pick_sheet =picks_models.PickSheet.objects.annotate_correct_count().get(
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
        pick_sheet =picks_models.PickSheet.objects.annotate_correct_count().get(
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
        pick_sheet =picks_models.PickSheet.objects.annotate_correct_count().get(
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
        other_pick_sheet = picks_factories.PickSheetFactory(
            pot=self.pot, picker="The Otherpicks_models.Picker"
        )
        picks_factories.PickFactory(
            pick_sheet=other_pick_sheet,
            game=self.game_1,
            picked_team=self.game_1_winning_team,
        )
        picks_factories.PickFactory(
            pick_sheet=other_pick_sheet,
            game=self.game_2,
            picked_team=self.game_2_winning_team,
        )
        assert picks_models.Pick.objects.count() == 4
        # Get the original pick, the one that is being tested
        pick_sheet =picks_models.PickSheet.objects.annotate_correct_count().get(
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
        pot = pots_factories.PotFactory(tiebreaker_score=score)
        pick_sheet = picks_factories.PickSheetFactory(pot=pot, tiebreaker_guess=guess)
        annotated_pick_sheets =picks_models.PickSheet.objects.annotate_tiebreaker_delta().filter(
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
        pot = pots_factories.PotFactory(tiebreaker_score=score)
        pick_sheet = picks_factories.PickSheetFactory(pot=pot, tiebreaker_guess=guess)
        annotated_pick_sheets = (
           picks_models.PickSheet.objects.annotate_tiebreaker_delta_abs().filter(pk=pick_sheet.id)
        )

        with django_assert_num_queries(1):
            result = annotated_pick_sheets[0].tiebreaker_delta_abs

        assert result == expected


@pytest.mark.django_db
class TestPick:
    @pytest.fixture
    def setup_game_with_two_teams(self):
        self.game = games_factories.Game(with_teams=True)
        self.team_1 = self.game.away_team
        self.team_2 = self.game.home_team

    def test_is_correct_annotation_is_true_if_picked_team_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.team_1
        self.game.set_and_save_winning_team(winning_team)
        pick = picks_factories.PickFactory(game=self.game, picked_team=winning_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick =picks_models.Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is True

    def test_is_correct_annotation_is_false_if_picked_team_not_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.team_1
        loosing_team = self.team_2
        self.game.set_and_save_winning_team(winning_team)
        pick = picks_factories.PickFactory(game=self.game, picked_team=loosing_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick =picks_models.Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is False

    def test_is_correct_annotation_with_tied_game(self, setup_game_with_two_teams):
        self.game.set_tie()
        self.game.save()
        assert self.game.winning_team is None
        assert self.game.is_tie is True
        pick_team_1 = picks_factories.PickFactory(game=self.game, picked_team=self.team_1)
        pick_team_2 = picks_factories.PickFactory(game=self.game, picked_team=self.team_2)
        pick_team_1 =picks_models.Pick.objects.annotate_is_correct().get(pk=pick_team_1.id)
        pick_team_2 =picks_models.Pick.objects.annotate_is_correct().get(pk=pick_team_2.id)

        result_team_1 = pick_team_1.is_correct
        result_team_2 = pick_team_2.is_correct

        assert result_team_1 is False
        assert result_team_2 is False
