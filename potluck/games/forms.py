from django import forms


from potluck.games.models import Game


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("teams",)
