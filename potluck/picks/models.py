from django.db import models

from potluck.games.models import Game
from potluck.teams.models import Team


class GamePick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_picks")
    pick = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+")
