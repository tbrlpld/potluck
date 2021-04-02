from django import forms


from potluck.games.models import Game


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("teams", "pot")
        widgets = {"pot": forms.HiddenInput()}
