from django.db import models
from django.core import validators
from django.core import exceptions

from potluck.teams.models import Team
from potluck.pots.models import Pot


class Game(models.Model):
    teams = models.ManyToManyField(
        Team,
        related_name="+",
        validators=[
            validators.MaxLengthValidator(limit_value=2),
            validators.MinLengthValidator(limit_value=2),
        ],
    )
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

    def clean_fields(self, exclude=None):
        errors = {}
        try:
            super().clean_fields(exclude=exclude)
        except exceptions.ValidationError as e:
            errors.update(e.message_dict)

        if not exclude or "teams" not in exclude:
            if self.teams.count() != 2:
                errors["teams"] = ["Please define exactly two teams."]

        if errors:
            raise exceptions.ValidationError(message=errors)

    # def get_team_names(self):
    #     teams = self.teams.values_list("id", "name")
    #     return [team[1] for team in teams]

    # def __str__(self):
    #     team_names = self.get_team_names()
    #     return " vs ".join(team_names)
