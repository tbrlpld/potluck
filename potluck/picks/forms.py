from django import forms

from potluck.picks.models import GamePick


class CreateGamePickForm(forms.ModelForm):
    class Meta:
        model = GamePick
        fields = ("game", "pick")
        widgets = {
            "game": forms.HiddenInput(),
        }
