import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.picks.models import Pick, PickSheet
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory
from potluck.teams.models import Team
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestPickSheet:
    @pytest.fixture
    def setup(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        team_3 = TeamFactory.create()
        team_4 = TeamFactory.create()
        self.pot = PotFactory.create()
        self.game_1 = GameFactory.create(pot=self.pot)
        self.game_1.teams.set((team_1, team_2))
        self.game_2 = GameFactory.create(pot=self.pot)
        self.game_2.teams.set((team_3, team_4))

        self.game_1_winning_team = self.game_1.teams.first()
        self.game_1_loosing_team = self.game_1.teams.last()
        self.game_1.winning_team = self.game_1_winning_team
        self.game_1.save()

        self.game_2_winning_team = self.game_2.teams.first()
        self.game_2_loosing_team = self.game_2.teams.last()
        self.game_2.winning_team = self.game_2_winning_team
        self.game_2.save()

        self.pick_sheet = PickSheetFactory.create(pot=self.pot)

        assert Pot.objects.count() == 1
        assert PickSheet.objects.count() == 1
        assert Game.objects.count() == 2
        assert Team.objects.count() == 4
        assert Pick.objects.count() == 0

        yield self

        Pot.objects.all().delete()
        PickSheet.objects.all().delete()
        Game.objects.all().delete()
        Team.objects.all().delete()

        assert Pot.objects.count() == 0
        assert PickSheet.objects.count() == 0
        assert Game.objects.count() == 0
        assert Team.objects.count() == 0
        assert Pick.objects.count() == 0

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

    def test_count_correct_method_returns_0_for_both_wrong(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 0

    def test_count_correct_method_returns_1_for_game_1_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 1

    def test_count_correct_method_returns_1_for_game_2_correct(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        result = self.pick_sheet.count_correct()

        assert result == 1

    def test_count_correct_method_returns_2_for_both_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):

        result = self.pick_sheet.count_correct()

        assert result == 2

    def test_correct_count_annotation_returns_0_for_both_wrong(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 0

    def test_correct_count_annotation_returns_1_for_game_1_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_1_for_game_2_correct(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(pk=self.pick_sheet.id)

        assert self.pick_sheet.count_correct() == 1
        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_2_for_both_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):
        pick_sheet = PickSheet.objects.annotate_correct_count().get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 2

    def test_correct_count_annotation_still_works_when_other_pick_in_db(
        self,
        setup,
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
        pick_sheet = PickSheet.objects.annotate_correct_count().get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 1


@pytest.mark.django_db
class TestPick:
    @pytest.fixture
    def setup_game_with_two_teams(self):
        self.team_1 = TeamFactory.create()
        self.team_2 = TeamFactory.create()
        self.game = GameFactory.create()
        self.game.teams.set((self.team_1, self.team_2))

    def test_is_correct_annotation_is_true_if_picked_team_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.game.teams.first()
        self.game.winning_team = winning_team
        self.game.save()  # Game needs to be able to check equality in the DB
        pick = PickFactory(game=self.game, picked_team=winning_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is True

    def test_is_correct_annotation_is_false_if_picked_team_not_matches_winning_team(
        self,
        setup_game_with_two_teams,
    ):
        winning_team = self.game.teams.first()
        loosing_team = self.game.teams.last()
        self.game.winning_team = winning_team
        self.game.save()  # Game needs to be able to check equality in the DB
        pick = PickFactory(game=self.game, picked_team=loosing_team)
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.annotate_is_correct().get(pk=pick.id)

        result = pick.is_correct

        assert result is False
