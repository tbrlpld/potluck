from django.db import models

from potluck.teams.models import Team
from potluck.pots.models import Pot


class Game(models.Model):
    teams = models.ManyToManyField(Team, related_name="+")
    winning_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )

    pot = models.ForeignKey(
        Pot,
        on_delete=models.CASCADE,
        related_name="games",
        blank=True,
        null=True,
    )

    def get_team_names(self):
        teams = self.teams.values_list("id", "name")[:2]
        return [team[1] for team in teams]

    def __str__(self):
        team_names = self.get_team_names()
        return f"{team_names[0]} vs {team_names[1]}"