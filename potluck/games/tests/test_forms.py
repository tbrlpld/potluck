import pytest

from potluck.games import forms as games_forms
from potluck.games import models as games_models
from potluck.games.tests import factories as games_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestCreateGame:
    def test_no_pot(self):
        with pytest.raises(TypeError):
            games_forms.CreateGame()

    def test_empty_form(self):
        pot = pots_factories.PotFactory()
        form = games_forms.CreateGame(pot=pot)

        result = form.is_valid()

        assert result is False
        assert form.pot == pot

    def test_with_empty_data(self):
        pot = pots_factories.PotFactory()
        form = games_forms.CreateGame(data={}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_empty_teams(self):
        pot = pots_factories.PotFactory()
        form = games_forms.CreateGame({"teams": []}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_one_team(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        form = games_forms.CreateGame(data={"teams": [team_1]}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_three_teams(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        team_2 = teams_factories.TeamFactory()
        team_3 = teams_factories.TeamFactory()
        form = games_forms.CreateGame(
            data={"teams": [team_1, team_2, team_3]},
            pot=pot,
        )

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_two_teams(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        team_2 = teams_factories.TeamFactory()
        form = games_forms.CreateGame(
            data={"teams": [team_1, team_2]},
            pot=pot,
        )

        result = form.is_valid()

        assert result is True
        assert "teams" not in form.errors
        assert "pot" not in form.errors
        game = form.save()
        assert game.pot == pot


@pytest.mark.django_db
class TestSetGameResult:
    @pytest.fixture
    def setup(self):
        self.game = games_factories.GameFactory()
        self.team_1 = teams_factories.TeamFactory()
        self.team_2 = teams_factories.TeamFactory()
        self.game.teams.set((self.team_1, self.team_2))

    def test_init_with_no_game(self):
        with pytest.raises(TypeError):
            games_forms.SetGameResult()

    def test_init_with_game_with_winning_team(self, setup):
        self.game.set_winning_team(self.team_1)

        form = games_forms.SetGameResult(
            game=self.game,
        )

        assert form.initial["result"] == self.team_1.id

    def test_init_with_game_is_tie(self, setup):
        self.game.set_tie()
        assert self.game.is_tie is True
        form = games_forms.SetGameResult(game=self.game)

        assert form.initial["result"] == form.TIE_VALUE

    def test_no_data(self, setup):
        form = games_forms.SetGameResult(
            game=self.game,
        )

        assert form.is_bound is False
        assert form.is_valid() is False

    def test_data_result_winning_team(self, setup):
        form = games_forms.SetGameResult(
            game=self.game,
            data={"result": self.team_1.id},
        )
        assert self.game.winning_team != self.team_1

        valid = form.is_valid()

        assert valid is True
        assert self.game.winning_team == self.team_1
        assert games_models.Game.objects.get(pk=self.game.id).winning_team != self.team_1

        form.save()

        assert games_models.Game.objects.get(pk=self.game.id).winning_team == self.team_1

    def test_data_result_winning_team_not_in_game(self, setup):
        team_not_in_game = teams_factories.TeamFactory()
        form = games_forms.SetGameResult(
            game=self.game,
            data={"result": team_not_in_game.id},
        )

        valid = form.is_valid()

        assert valid is False
        assert "result" in form.errors

    def test_data_result_tie(self, setup):
        form = games_forms.SetGameResult(
            data={"result": games_forms.SetGameResult.TIE_VALUE},
            game=self.game,
        )
        assert self.game.is_tie is not True

        valid = form.is_valid()

        assert valid is True
        assert self.game.is_tie is True
        assert games_models.Game.objects.get(pk=self.game.id).is_tie != True

        form.save()

        assert games_models.Game.objects.get(pk=self.game.id).is_tie == True

    def test_setting_team_unsets_tie(self, setup):
        self.game.set_tie()
        assert self.game.is_tie is True

        games_forms.SetGameResult(
            data={"result": self.team_1.id},
            game=self.game,
        )

        assert self.game.is_tie is not True
        assert self.game.is_tie is False
        assert self.game.winning_team == self.team_1

    def test_setting_tie_unsets_team(self, setup):
        self.game.set_winning_team(self.team_1)
        assert self.game.winning_team == self.team_1
        assert self.game.is_tie is False

        games_forms.SetGameResult(
            data={"result": games_forms.SetGameResult.TIE_VALUE},
            game=self.game,
        )

        assert self.game.winning_team != self.team_1
        assert self.game.winning_team is None
        assert self.game.is_tie is True

    def test_tie_value(self):
        assert games_forms.SetGameResult.TIE_VALUE == -1

    def test_tie_label(self):
        assert games_forms.SetGameResult.TIE_LABEL == "Tie"

    def test_tie_choice(self):
        assert games_forms.SetGameResult.TIE_CHOICE == (
            games_forms.SetGameResult.TIE_VALUE,
            games_forms.SetGameResult.TIE_LABEL,
        )

    def test_result_choices(self, setup):
        form = games_forms.SetGameResult(game=self.game)

        choices = form.fields["result"].choices
        assert (self.team_1.id, self.team_1.name) in choices
        assert (self.team_2.id, self.team_2.name) in choices
        assert form.TIE_CHOICE in choices
