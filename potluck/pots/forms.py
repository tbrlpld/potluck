from django import forms
from django.core import validators

from potluck.games.models import Game, Team
from potluck.pots.models import Pot


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
        fields = ("teams",)

    def __init__(self, *args, pot, **kwargs):
        self.pot = pot
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.pot = self.pot
        return super().save(*args, **kwargs)
