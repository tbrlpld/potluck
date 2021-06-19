from django.db import models


class Pot(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)

    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        OPEN = "OP", "Open"
        CLOSED = "CL", "Closed"
        TALLY = "TA", "Tally"

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    def __str__(self):
        return self.name

    def get_tally(self):
        return self.pick_sheets.order_by("-correct_count")
