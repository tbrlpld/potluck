from django import forms

from potluck.picks import models as picks_models


class CreatePickSheet(forms.ModelForm):
    class Meta:
        model = picks_models.PickSheet
        fields = ("picker", "tiebreaker_guess")
        labels = {"picker": "Your name"}

    def __init__(self, *args, pot, **kwargs):
        super().__init__(*args, **kwargs)
        self.pot = pot

    def save(self, *args, **kwargs):
        self.instance.pot = self.pot
        return super().save(*args, **kwargs)


class CreatePick(forms.ModelForm):
    class Meta:
        model = picks_models.Pick
        fields = ("picked_team",)
        widgets = {
            "picked_team": forms.RadioSelect,
        }

    def __init__(self, *args, game, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.fields["picked_team"].queryset = self.game.get_teams()

    def save(self, *args, **kwargs):
        self.instance.game = self.game
        return super().save(*args, **kwargs)


class BaseCreatePickFormset(forms.BaseFormSet):
    def __init__(self, *args, games, **kwargs):
        self.games = games
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["game"] = self.games[index]
        return kwargs
