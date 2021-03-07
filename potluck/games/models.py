from django.db import models

from potluck.teams.models import Team


# class GameTeam(models.Model):
#     """Through model to connect a game and a team."""

#     pass


class Game(models.Model):
    teams = models.ManyToManyField(Team, related_name="+")
    winning_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )
