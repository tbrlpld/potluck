from django import forms
from django.core import validators

from potluck.games.models import Game
from potluck.games.models import Team


class GameAddForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        validators=[
            validators.MaxLengthValidator(limit_value=2),
            validators.MinLengthValidator(limit_value=2),
        ],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Game
        fields = ("teams", "pot")
        widgets = {"pot": forms.HiddenInput()}
