import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.picks.models import GamePick, Pick
from potluck.picks.tests.factories import GamePickFactory, PickFactory
from potluck.teams.models import Team


@pytest.mark.django_db
class TestPick:

    @pytest.fixture
    def setup(self):
        self.pick = PickFactory.create()
        self.game_1 = self.pick.pot.games.first()
        self.game_2 = self.pick.pot.games.last()

        self.game_1_winning_team = self.game_1.teams.first()
        self.game_1_loosing_team = self.game_1.teams.last()
        self.game_1.winning_team = self.game_1_winning_team
        self.game_1.save()

        self.game_2_winning_team = self.game_2.teams.first()
        self.game_2_loosing_team = self.game_2.teams.last()
        self.game_2.winning_team = self.game_2_winning_team
        self.game_2.save()

        assert Pick.objects.count() == 1
        assert Game.objects.count() == 2
        assert Team.objects.count() == 4
        assert GamePick.objects.count() == 0

        yield self

        Pick.objects.all().delete()
        Game.objects.all().delete()
        Team.objects.all().delete()

        assert Pick.objects.count() == 0
        assert Game.objects.count() == 0
        assert Team.objects.count() == 0
        assert GamePick.objects.count() == 0

    @pytest.fixture
    def place_game_1_wrong_pick(self):
        game_pick = GamePickFactory.create(
            pick=self.pick, game=self.game_1, picked_team=self.game_1_loosing_team
        )

        yield game_pick

        game_pick.delete()

    @pytest.fixture
    def place_game_1_correct_pick(self):
        game_pick = GamePickFactory.create(
            pick=self.pick, game=self.game_1, picked_team=self.game_1_winning_team
        )

        yield game_pick

        game_pick.delete()

    @pytest.fixture
    def place_game_2_wrong_pick(self):
        game_pick = GamePickFactory.create(
            pick=self.pick, game=self.game_2, picked_team=self.game_2_loosing_team
        )

        yield game_pick

        game_pick.delete()

    @pytest.fixture
    def place_game_2_correct_pick(self):
        game_pick = GamePickFactory.create(
            pick=self.pick, game=self.game_2, picked_team=self.game_2_winning_team
        )

        yield game_pick

        game_pick.delete()

    def test_count_correct_method_returns_0_for_both_wrong(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):

        result = self.pick.count_correct()

        assert result == 0

    def test_count_correct_method_returns_1_for_game_1_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):

        result = self.pick.count_correct()

        assert result == 1

    def test_count_correct_method_returns_1_for_game_2_correct(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):

        result = self.pick.count_correct()

        assert result == 1

    def test_count_correct_method_returns_2_for_both_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):

        result = self.pick.count_correct()

        assert result == 2

    def test_correct_count_annotation_returns_0_for_both_wrong(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_wrong_pick,
    ):

        assert GamePick.objects.count() == 2
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=self.pick.id)

        result = pick.correct_count

        assert result == 0

    def test_correct_count_annotation_returns_1_for_game_1_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_wrong_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=self.pick.id)

        result = pick.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_1_for_game_2_correct(
        self,
        setup,
        place_game_1_wrong_pick,
        place_game_2_correct_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=self.pick.id)
        # pick = Pick.objects.all().annotate_correct_count().filter(pk=self.pick.id)[0]

        assert self.pick.count_correct() == 1

        # from django.db import models

        # correct_game_picks = GamePick.objects.filter(
        #     pick=models.OuterRef("pk"),
        #     is_correct=True
        # ).values("pick_id").annotate(count=models.Count("pk")).values("pk")
        # annotated_picks = Pick.objects.annotate(
        #     correct_count=models.Subquery(correct_game_picks)
        # )

        # result = annotated_picks.filter(pk=self.pick.id)[0].correct_count
        result = pick.correct_count

        assert result == 1

    def test_correct_count_annotation_returns_2_for_both_correct(
        self,
        setup,
        place_game_1_correct_pick,
        place_game_2_correct_pick,
    ):
        # To get the annotation, you need to retrieve the object from the manager
        pick = Pick.objects.get(pk=self.pick.id)

        result = pick.correct_count

        assert result == 2


@ pytest.mark.django_db
class TestGamePick:
    def test_is_correct_annotation_is_true_if_picked_team_matches_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        game.winning_team = winning_team
        game.save()  # Game needs to be able to check equality in the DB
        game_pick = GamePickFactory(
            game=game,
            picked_team=winning_team
        )
        # To get the annotation, you need to retrieve the object from the manager
        game_pick = GamePick.objects.get(pk=game_pick.id)

        result = game_pick.is_correct

        assert result is True

    def test_is_correct_annotation_is_false_if_picked_team_not_matches_winning_team(self):
        game = GameFactory.create()
        winning_team = game.teams.first()
        loosing_team = game.teams.last()
        game.winning_team = winning_team
        game.save()  # Game needs to be able to check equality in the DB
        game_pick = GamePickFactory(
            game=game,
            picked_team=loosing_team
        )
        # To get the annotation, you need to retrieve the object from the manager
        game_pick = GamePick.objects.get(pk=game_pick.id)

        result = game_pick.is_correct

        assert result is False
