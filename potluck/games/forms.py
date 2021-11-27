from django import forms
from django.core import validators

from potluck.games import models as games_models
from potluck.teams import models as teams_models


class CreateGame(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=teams_models.Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(2),
        ],
    )

    class Meta:
        model = games_models.Game
        fields = ("teams",)

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

    winning_team = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    def __init__(self, *, data=None, game, **kwargs):
        self.game = game

        initial = kwargs.get("initial", {})
        if self.game.winning_team:
            initial["winning_team"] = self.game.winning_team.id

        super().__init__(data, initial=initial, **kwargs)

        winning_team_field_name = self["winning_team"].html_name
        if data and winning_team_field_name in data:
            team_id = int(data[winning_team_field_name])
            self.game.winning_team = teams_models.Team.objects.get(pk=team_id)

        self.fields["winning_team"].choices = self.get_choices(
            game=self.game
        )

    @staticmethod
    def get_choices(*, game):
        choices = [
            (team.id, team.name)
            for team in game.teams.all()
        ]
        return choices

    def save(self):
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
