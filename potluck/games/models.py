from django.db import models

from potluck.teams.models import Team


# class GameTeam(models.Model):
#     """Through model to connect a game and a team."""

#     pass


class Game(models.Model):
    teams = models.ManyToManyField(Team, related_name="+")
    winner = models.ForeignKey(
        Team, limit_choices_to=teams, on_delete=models.CASCADE, related_name="+"
    )
