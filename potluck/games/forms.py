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
    winning_team = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    def __init__(self, *, data=None, instance, **kwargs):
        self.instance = instance

        initial = kwargs.get("initial", {})
        if self.instance.winning_team:
            initial["winning_team"] = self.instance.winning_team.id

        if data and "winning_team" in data:
            team_id = int(data["winning_team"])
            self.instance.winning_team = teams_models.Team.objects.get(pk=team_id)

        super().__init__(data, initial=initial, **kwargs)

        self.fields["winning_team"].choices = self.get_choices(
            game=self.instance
        )

    @staticmethod
    def get_choices(*, game):
        choices = [
            (team.id, team.name)
            for team in game.teams.all()
        ]
        return choices
