from django.core import exceptions
from django.db import models

from potluck.pots import models as pots_models
from potluck.teams import models as teams_models


class Game(models.Model):
    home_team = models.ForeignKey(
        teams_models.Team,
        related_name="+",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    away_team = models.ForeignKey(
        teams_models.Team,
        related_name="+",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

    # Deprecated. Do not use.
    teams = models.ManyToManyField(
        teams_models.Team,
        related_name="+",
    )

    winning_team = models.ForeignKey(
        teams_models.Team,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )
    is_tie = models.BooleanField(
        null=True,
        blank=True,
    )

    pot = models.ForeignKey(
        pots_models.Pot,
        on_delete=models.CASCADE,
        related_name="games",
        null=True,
        blank=False,
    )

    def __str__(self) -> str:
        team_names = self.get_team_names()
        return " vs ".join(team_names)

    def get_teams(self) -> models.QuerySet[teams_models.Team]:
        team_ids = [team.id for team in (self.home_team, self.away_team) if team is not None]
        return teams_models.Team.objects.filter(pk__in=team_ids)

    def get_team_names(self) -> list[str]:
        teams = self.teams.values_list("id", "name")
        return [team[1] for team in teams]

    def set_winning_team(self, team: teams_models.Team) -> None:
        self.winning_team = team
        if self.is_tie is not False:
            self.is_tie = False

    def set_and_save_winning_team(self, team: teams_models.Team) -> None:
        self.set_winning_team(team)
        self.clean()
        self.save()

    def set_tie(self) -> None:
        if self.winning_team is not None:
            self.winning_team = None
        self.is_tie = True

    def clean(self) -> None:
        if self.winning_team and self.is_tie:
            raise exceptions.ValidationError(
                "Winning team and tie are mutually exclusive. Set only either one."
            )
        if self.winning_team and self.winning_team not in self.teams.all():
            raise exceptions.ValidationError("Team has to paricipate in game to win!")
