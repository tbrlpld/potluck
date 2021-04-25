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


class GamePickQueryset(models.QuerySet):
    def annotate_is_correct(self):
        return self.annotate(
            is_correct=models.ExpressionWrapper(
                models.Q(picked_team=models.F("game__winning_team")),
                output_field=models.BooleanField(),
            )
        )


class GamePickManager(models.Manager):
    def get_queryset(self):
        queryset = GamePickQueryset(self.model, using=self._db)
        queryset = queryset.annotate_is_correct()
        return queryset


class GamePick(models.Model):
    pick = models.ForeignKey(
        Pick, on_delete=models.CASCADE, related_name="game_picks", null=True, blank=True
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="game_picks")
    picked_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="+", null=True, blank=False
    )

    objects = GamePickManager.from_queryset(GamePickQueryset)()

    def __str__(self):
        return f"GamePick {self.id} for {self.pick}: {self.game}"

    def add_pick(self, pick):
        self.pick = pick
        self.full_clean
        self.save()

    # def is_correct(self):
    #     """Return true if picked team is game's winning team."""
    #     return self.picked_team == self.game.winning_team
