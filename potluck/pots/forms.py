from django import forms
from django.core import validators

from potluck.pots.models import Pot
from potluck.games.models import Game, Team


class SetTiebreakerScoreForm(forms.ModelForm):
    class Meta:
        model = Pot
        fields = ("tiebreaker_score",)


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
        fields = ("teams", "pot")
        widgets = {"pot": forms.HiddenInput()}
