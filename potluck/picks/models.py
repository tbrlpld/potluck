from django.db import models

from potluck.games.models import Game
from potluck.pots.models import Pot
from potluck.teams.models import Team


class PickSheetQueryset(models.QuerySet):
    def annotate_correct_count(self):
        correct_picks = Pick.objects.filter(
            is_correct=True,
        )
        annotated_pick_sheets = self.annotate(
            correct_count=models.Count(
                "picks",
                filter=models.Q(picks__in=correct_picks),
                distinct=True
            )
        )
        return annotated_pick_sheets


class PickSheetManager(models.Manager):
    def get_queryset(self):
        queryset = PickSheetQueryset(self.model, using=self._db)
        queryset = queryset.annotate_correct_count()
        return queryset


PickSheetMangerFromQueryset = PickSheetManager.from_queryset(PickSheetQueryset)


class PickSheet(models.Model):
    picker = models.CharField(max_length=100, help_text="Name of the person picking")
    pot = models.ForeignKey(Pot, on_delete=models.CASCADE, related_name="picks")

    objects = PickSheetMangerFromQueryset()

    def __str__(self):
        return f"PickSheet {self.id}: {self.picker} ({self.pot})"

    def count_correct(self):
        correct_game_picks = self.picks.filter(is_correct=True)
        # print(corrent_game_picks.query)
        return correct_game_picks.count()


class PickQueryset(models.QuerySet):
    def annotate_is_correct(self):
        return self.annotate(
            is_correct=models.ExpressionWrapper(
                models.Q(picked_team=models.F("game__winning_team")),
                output_field=models.BooleanField(),
            )
        )


class PickManager(models.Manager):
    def get_queryset(self):
        queryset = PickQueryset(self.model, using=self._db)
        queryset = queryset.annotate_is_correct()
        return queryset


PickMangerFromQueryset = PickManager.from_queryset(PickQueryset)


class Pick(models.Model):
    pick_sheet = models.ForeignKey(
        PickSheet,
        on_delete=models.CASCADE,
        related_name="picks",
        null=True,
        blank=True,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="picks",
    )
    picked_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=False,
    )

    objects = PickMangerFromQueryset()

    def __str__(self):
        return f"Pick {self.id}: {self.pick_sheet.picker} ({self.game})"

    def add_pick_sheet(self, pick_sheet):
        self.pick_sheet = pick_sheet
        self.full_clean
        self.save()

    def check_if_correct(self):
        """Return true if picked team is game's winning team."""
        return self.picked_team == self.game.winning_team
