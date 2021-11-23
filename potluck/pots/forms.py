from django import forms

from potluck.pots import models as pots_models


class SetTiebreakerScore(forms.ModelForm):
    class Meta:
        model = pots_models.Pot
        fields = ("tiebreaker_score",)
