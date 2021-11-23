from django import forms

from potluck.pots.models import Pot


class SetTiebreakerScoreForm(forms.ModelForm):
    class Meta:
        model = Pot
        fields = ("tiebreaker_score",)
