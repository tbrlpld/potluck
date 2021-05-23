from django import forms

from potluck.picks.models import GamePickTemp, PickSheet


class CreatePickForm(forms.ModelForm):
    class Meta:
        model = PickSheet
        fields = ("picker", "pot")
        widgets = {
            "pot": forms.HiddenInput(),
        }
        labels = {"picker": "Your name"}


class CreateGamePickForm(forms.ModelForm):
    class Meta:
        model = GamePickTemp
        fields = ("game", "picked_team")
        widgets = {
            "game": forms.HiddenInput(),
            "picked_team": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = self.initial.get("game")
        if self.game is None:
            raise ValueError(
                "{0} needs receive a game as initial data.".format(
                    self.__class__))
        self.fields["picked_team"].queryset = self.game.teams
        self.fields["picked_team"].label = str(self.game)


# GamePickFormset = forms.formset_factory(CreateGamePickForm, extra=0)
