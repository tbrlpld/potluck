import pytest

from potluck.games import forms as games_forms
from potluck.games import models as games_models
from potluck.games import factories as games_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestCreateGame:
    @pytest.fixture
    def setup(self):
        self.pot = pots_factories.PotFactory()

    def test_no_pot(self):
        with pytest.raises(TypeError):
            games_forms.CreateGame()

    def test_empty_form(self, setup):
        form = games_forms.CreateGame(pot=self.pot)

        result = form.is_valid()

        assert result is False
        assert form.pot == self.pot

    def test_data_empty(self, setup):
        form = games_forms.CreateGame(data={}, pot=self.pot)

        result = form.is_valid()

        assert result is False
        assert "home_team" in form.errors
        assert "away_team" in form.errors

    def test_data_home_team_only(self, setup):
        home_team = teams_factories.TeamFactory()
        data = {"home_team": home_team}
        form = games_forms.CreateGame(data=data, pot=self.pot)

        result = form.is_valid()

        assert result is False
        assert "away_team" in form.errors

    def test_data_away_team_only(self, setup):
        away_team = teams_factories.TeamFactory()
        data = {"away_team": away_team}
        form = games_forms.CreateGame(data=data, pot=self.pot)

        result = form.is_valid()

        assert result is False
        assert "home_team" in form.errors

    def test_data_home_and_away_team(self, setup):
        home_team = teams_factories.TeamFactory()
        away_team = teams_factories.TeamFactory()
        data = {"home_team": home_team, "away_team": away_team}
        form = games_forms.CreateGame(data=data, pot=self.pot)

        result = form.is_valid()

        assert result is True

        game = form.save()

        assert game.pot == self.pot
        assert game.home_team == home_team
        assert game.away_team == away_team

    # TODO: Test home and away team the same


@pytest.mark.django_db
class TestSetGameResult:
    @pytest.fixture
    def setup(self):
        self.game = games_factories.Game()
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
        assert (
            games_models.Game.objects.get(pk=self.game.id).winning_team != self.team_1
        )

        form.save()

        assert (
            games_models.Game.objects.get(pk=self.game.id).winning_team == self.team_1
        )

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
        assert games_models.Game.objects.get(pk=self.game.id).is_tie is not True

        form.save()

        assert games_models.Game.objects.get(pk=self.game.id).is_tie is True

    def test_setting_team_unsets_tie(self, setup):
        self.game.set_tie()
        assert self.game.is_tie is True
        form = games_forms.SetGameResult(
            data={"result": self.team_1.id},
            game=self.game,
        )

        valid = form.is_valid()

        assert valid is True
        assert self.game.is_tie is False
        assert self.game.winning_team == self.team_1

    def test_setting_tie_unsets_team(self, setup):
        self.game.set_winning_team(self.team_1)
        assert self.game.winning_team == self.team_1
        assert self.game.is_tie is False
        form = games_forms.SetGameResult(
            data={"result": games_forms.SetGameResult.TIE_VALUE},
            game=self.game,
        )

        valid = form.is_valid()

        assert valid is True
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
