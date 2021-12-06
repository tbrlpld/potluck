from typing import Any, Optional

from django import forms

from potluck.games import models as games_models
from potluck.teams import models as teams_models


class CreateGame(forms.ModelForm):
    class Meta:
        model = games_models.Game
        fields = ("home_team", "away_team")

    def __init__(self, *args, pot, **kwargs):
        self.pot = pot
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.pot = self.pot
        return super().save(*args, **kwargs)


class SetGameResult(forms.Form):
    """
    Form to set the result of a game.

    This is implemented with a custom form instead of a ModelForm to allow for using
    the same choice field to select between the teams of the game or a tie.

    On the model, the tie is set as a separate field but it makes more sense on the
    form to have that as a single radio select.

    """

    TIE_VALUE = -1
    TIE_LABEL = "Tie"
    TIE_CHOICE = (TIE_VALUE, TIE_LABEL)

    result = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    def __init__(
        self,
        *,
        data: Optional[dict] = None,
        game: games_models.Game,
        **kwargs,
    ) -> None:
        self.game = game

        initial = kwargs.get("initial", {})
        if self.game.winning_team:
            initial["result"] = self.game.winning_team.id
        elif self.game.is_tie:
            initial["result"] = self.TIE_VALUE

        super().__init__(data, initial=initial, **kwargs)

        self.fields["result"].choices = self.get_result_choices(game=self.game)

    def get_result_choices(self, *, game: games_models.Game) -> list[tuple[int, str]]:
        choices = [(team.id, team.name) for team in game.get_teams()]
        choices.append(self.TIE_CHOICE)
        return choices

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        result = cleaned_data.get("result")
        if result and self.has_changed():
            result_int = int(result)
            if result_int == self.TIE_VALUE:
                self.game.set_tie()
            else:
                self.game.set_winning_team(teams_models.Team.objects.get(pk=result_int))

        return cleaned_data

    def save(self) -> games_models.Game:
        self.game.save()
        return self.game


class BaseSetGameResultFormSet(forms.BaseFormSet):
    def __init__(self, *args, games, **kwargs):
        self.games = games
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["game"] = self.games[index]
        return kwargs
