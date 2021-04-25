from django.db import models

from potluck.games.models import Game
from potluck.pots.models import Pot
from potluck.teams.models import Team


class Pick(models.Model):
    picker = models.CharField(max_length=100, help_text="Name of the person picking")
    pot = models.ForeignKey(Pot, on_delete=models.CASCADE, related_name="picks")

    def __str__(self):
        return f"Pick {self.id}: {self.pot} - {self.picker}"

    def count_correct(self):
        return len([
            game_pick for game_pick in self.game_picks.all()
            if game_pick.is_correct()
        ])


class GamePick(models.Model):
    pick = models.ForeignKey(
        Pick, on_delete=models.CASCADE, related_name="game_picks", null=True, blank=True
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_picks")
    picked_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="+", null=True, blank=False
    )

    def __str__(self):
        return f"GamePick {self.id} for {self.pick}: {self.game}"

    def add_pick(self, pick):
        self.pick = pick
        self.full_clean
        self.save()

    def is_correct(self):
        """Return true if picked team is game's winning team."""
        return self.picked_team == self.game.winning_team
