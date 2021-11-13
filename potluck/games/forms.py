from django import forms

from potluck.games.models import Game


class SetWinningTeamForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("winning_team",)
        widgets = {"winning_team": forms.RadioSelect}

    def __init__(self, *args, initial=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["winning_team"].queryset = self.instance.teams
        self.fields["winning_team"].empty_label = None
