from django import forms


from potluck.games.models import Game


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("teams",)

    def clean_teams(self):
        data = self.cleaned_data["teams"]
        if len(data) != 2:
            raise forms.ValidationError("Please select two teams.")
        return data
