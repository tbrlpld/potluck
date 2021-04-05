from django import forms

from potluck.games.models import Game
from potluck.games.models import Team


class GameAddForm(forms.ModelForm):
    # teams = forms.ModelMultipleChoiceField(
    #     queryset=Team.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )

    class Meta:
        model = Game
        fields = ("teams", "pot")
        widgets = {"pot": forms.HiddenInput()}
