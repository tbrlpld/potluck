from django import forms
from django.core import validators

from potluck.pots.models import Pot
from potluck.games.models import Game, Team


class SetTiebreakerScoreForm(forms.ModelForm):
    class Meta:
        model = Pot
        fields = ("tiebreaker_score",)


class GameAddForm(forms.ModelForm):
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
        fields = ("teams", "pot")
        widgets = {"pot": forms.HiddenInput()}


class SetWinningTeamForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("winning_team",)
        widgets = {"winning_team": forms.RadioSelect}

    def __init__(self, *args, initial=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["winning_team"].queryset = self.instance.teams
        self.fields["winning_team"].empty_label = None
