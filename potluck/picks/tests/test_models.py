import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import GamePick
from potluck.picks.tests.factories import GamePickFactory, PickFactory


@pytest.mark.django_db
class TestPick:
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

    def place_game_1_wrong_pick(self):
        GamePickFactory(
            pick=self.pick, game=self.game_1, picked_team=self.game_1_loosing_team
        )

    def place_game_1_correct_pick(self):
        GamePickFactory(
            pick=self.pick, game=self.game_1, picked_team=self.game_1_winning_team
        )

    def place_game_2_wrong_pick(self):
        GamePickFactory(
            pick=self.pick, game=self.game_2, picked_team=self.game_2_loosing_team
        )

    def place_game_2_correct_pick(self):
        GamePickFactory(
            pick=self.pick, game=self.game_2, picked_team=self.game_2_winning_team
        )

    def test_count_correct_returns_0_for_both_wrong(self):
        self.place_game_1_wrong_pick()
        self.place_game_2_wrong_pick()

        result = self.pick.count_correct()

        assert result == 0

    def test_count_correct_returns_1_for_game_1_correct(self):
        self.place_game_1_correct_pick()
        self.place_game_2_wrong_pick()

        result = self.pick.count_correct()

        assert result == 1

    def test_count_correct_returns_1_for_game_2_correct(self):
        self.place_game_1_wrong_pick()
        self.place_game_2_correct_pick()

        result = self.pick.count_correct()

        assert result == 1

    def test_count_correct_returns_2_for_both_correct(self):
        self.place_game_1_correct_pick()
        self.place_game_2_correct_pick()

        result = self.pick.count_correct()

        assert result == 2


@pytest.mark.django_db
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
