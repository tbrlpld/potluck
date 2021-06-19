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
        null=False,
    )
    status_order = (
        Status.DRAFT,
        Status.OPEN,
        Status.CLOSED,
        Status.TALLY,
    )

    def __str__(self):
        return self.name

    def get_tally(self):
        return self.pick_sheets.order_by("-correct_count")

    @property
    def next_status(self):
        next_status_index = self.status_order.index(self.status) + 1
        try:
            next_status = self.status_order[next_status_index]
        except IndexError:
            next_status = None
        return next_status

    @property
    def previous_status(self):
        previous_status_index = self.status_order.index(self.status) - 1
        if previous_status_index < 0:
            previous_status = None
        else:
            previous_status = self.status_order[previous_status_index]
        return previous_status
