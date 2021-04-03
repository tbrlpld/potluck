from django import forms

from potluck.picks.models import GamePick


class CreateGamePickForm(forms.ModelForm):
    class Meta:
        model = GamePick
        fields = ("game", "pick")
        widgets = {
            "game": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game = self.initial.get("game")
        if game is None:
            raise ValueError(
                "{0} needs receive a game as initial data.".format(self.__class__)
            )
        self.fields["pick"].queryset = self.initial["game"].teams
