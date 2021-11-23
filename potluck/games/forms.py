from django import forms
from django.core import validators

from potluck.games.models import Game
from potluck.teams.models import Team


class CreateGameInPotForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(2),
        ],
    )

    class Meta:
        model = Game
        fields = ("teams",)

    def __init__(self, *args, pot, **kwargs):
        self.pot = pot
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.pot = self.pot
        return super().save(*args, **kwargs)


class SetWinningTeamForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("winning_team",)
        widgets = {"winning_team": forms.RadioSelect}

    def __init__(self, *args, initial=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["winning_team"].queryset = self.instance.teams
        self.fields["winning_team"].empty_label = None
