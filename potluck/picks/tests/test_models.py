import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.picks.models import Pick, PickSheet
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.teams.models import Team


@pytest.mark.django_db
class TestPick:

    @pytest.fixture
    def setup(self):
        self.pick_sheet = PickSheetFactory.create()
        self.pot = self.pick_sheet.pot
        self.game_1 = self.pot.games.first()
        self.game_2 = self.pot.games.last()

        self.game_1_winning_team = self.game_1.teams.first()
        self.game_1_loosing_team = self.game_1.teams.last()
        self.game_1.winning_team = self.game_1_winning_team
        self.game_1.save()

        self.game_2_winning_team = self.game_2.teams.first()
        self.game_2_loosing_team = self.game_2.teams.last()
        self.game_2.winning_team = self.game_2_winning_team
        self.game_2.save()

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
            pick_sheet=self.pick_sheet, game=self.game_1, picked_team=self.game_1_loosing_team
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_1_correct_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet, game=self.game_1, picked_team=self.game_1_winning_team
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_wrong_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet, game=self.game_2, picked_team=self.game_2_loosing_team
        )

        yield pick

        pick.delete()

    @pytest.fixture
    def place_game_2_correct_pick(self):
        pick = PickFactory.create(
            pick_sheet=self.pick_sheet, game=self.game_2, picked_team=self.game_2_winning_team
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
        # To get the annotation, you need to retrieve the object from the manager
        pick_sheet = PickSheet.objects.get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 0

    def test_correct_count_annotation_returns_1_for_game_1_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick_sheet = PickSheet.objects.get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_1_for_game_2_correct(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick_sheet = PickSheet.objects.get(pk=self.pick_sheet.id)

        assert self.pick_sheet.count_correct() == 1
        result = pick_sheet.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_2_for_both_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick_sheet = PickSheet.objects.get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 2

    def test_correct_count_annotation_still_works_when_other_pick_in_db(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        # Create another pick with 2 correct picks. It's existence can not incluence the fact
        # that the pick under test only has one correct pick!
        other_pick_sheet = PickSheetFactory.create(pot=self.pot, picker="The Other Picker")
        PickFactory.create(
            pick_sheet=other_pick_sheet, game=self.game_1, picked_team=self.game_1_winning_team
        )
        PickFactory.create(
            pick_sheet=other_pick_sheet, game=self.game_2, picked_team=self.game_2_winning_team
        )
        assert Pick.objects.count() == 4
        # Get the original pick, the one that is being tested
        pick_sheet = PickSheet.objects.get(pk=self.pick_sheet.id)

        result = pick_sheet.correct_count

        assert result == 1

    # def test_annotation(self):
    #     team_1 = Team(name="Test Team 1")
    #     team_1.save()
    #     team_2 = Team(name="Test Team 2")
    #     team_2.save()
    #     team_3 = Team(name="Test Team 3")
    #     team_3.save()
    #     team_4 = Team(name="Test Team 4")
    #     team_4.save()
    #     team_5 = Team(name="Test Team 5")
    #     team_5.save()
    #     team_6 = Team(name="Test Team 6")
    #     team_6.save()
    #     assert Team.objects.count() == 6

    #     pot = Pot(name="Test Pot")
    #     pot.save()
    #     assert Pot.objects.count() == 1
    #     assert Pot.objects.first() == pot

    #     game_1 = Game(pot=pot)
    #     game_1.save()
    #     game_1.teams.add(team_1, team_2)
    #     game_1.winning_team = team_1
    #     game_1.save()
    #     game_2 = Game(pot=pot)
    #     game_2.save()
    #     game_2.teams.add(team_3, team_4)
    #     game_2.winning_team = team_3
    #     game_2.save()
    #     game_3 = Game(pot=pot)
    #     game_3.save()
    #     game_3.teams.add(team_5, team_6)
    #     game_3.winning_team = team_5
    #     game_3.save()
    #     assert Game.objects.count() == 3
    #     assert pot.games.count() == 3
    #     assert pot.games.all()[0].winning_team == team_1
    #     assert pot.games.all()[1].winning_team == team_3
    #     assert pot.games.all()[2].winning_team == team_5

    #     pick = Pick(picker="Tester", pot=pot)
    #     pick.save()
    #     assert Pick.objects.count() == 1

    #     game_pick_1 = GamePick(pick=pick, game=game_1, picked_team=team_1)
    #     game_pick_1.save()
    #     game_pick_2 = GamePick(pick=pick, game=game_2, picked_team=team_3)
    #     game_pick_2.save()
    #     game_pick_3 = GamePick(pick=pick, game=game_3, picked_team=team_5)
    #     game_pick_3.save()

    #     assert GamePick.objects.count() == 3
    #     assert pick.game_picks.count() == 3
    #     assert pick.game_picks.all()[0].is_correct == True
    #     assert pick.game_picks.all()[1].is_correct == True
    #     assert pick.game_picks.all()[2].is_correct == True
    #     assert pick.count_correct() == 3

    #     from django.db import models

    #     correct_game_picks = GamePick.objects.filter(
    #         is_correct=True,
    #     )

    #     picks = Pick.objects.all().annotate(
    #         correct_count=models.Count(
    #             "game_picks",
    #             filter=models.Q(game_picks__in=correct_game_picks),
    #             distinct=True
    #         )
    #     )

    #     pick = picks[0]

    #     assert correct_game_picks.count() == 3
    #     assert pick.correct_count == 3

@ pytest.mark.django_db
class TestGamePick:
    def test_is_correct_annotation_is_true_if_picked_team_matches_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        game.winning_team = winning_team
        game.save()  # Game needs to be able to check equality in the DB
        pick = PickFactory(
            game=game,
            picked_team=winning_team
        )
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=pick.id)

        result = pick.is_correct

        assert result is True

    def test_is_correct_annotation_is_false_if_picked_team_not_matches_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        loosing_team = game.teams.last()
        game.winning_team = winning_team
        game.save()  # Game needs to be able to check equality in the DB
        pick = PickFactory(
            game=game,
            picked_team=loosing_team
        )
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=pick.id)

        result = pick.is_correct

        assert result is False
