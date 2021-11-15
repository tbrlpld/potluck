from django.db import models


class Pot(models.Model):
    name = models.CharField(
        max_length=250, null=False, blank=False, help_text="What shall we call the pot?"
    )
    tiebreaker_description = models.CharField(
        max_length=500,       null=False,
        blank=False,
        help_text=(
            "Describe the tiebreaker score you want to use for the pot. "
            'For example: "Total score of the Monday night game". '
            "In case of a tie, the submission with the closest guess to the score wins."
        ),
        default="Total score of the Monday night game",
    )
    tiebreaker_score = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Enter the score for the tiebreaker."
    )

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
    _next_status_action_text = {
        Status.OPEN: "Open up the pot for pick submission",
        Status.CLOSED: "Close the pot and set winning teams",
        Status.TALLY: "Finish off the pot and check who won",
    }
    _previous_status_action_text = {
        Status.DRAFT: "Reset the pot to draft to edit the games",
        Status.OPEN: "Re-open up the pot for pick submissions",
        Status.CLOSED: "Go back to set winning teams in the games",
    }
    _status_help_text = {
        Status.DRAFT: (
            "While the pot is in draft you can "
            "add and remove games included in the pot. "
            "No picks can be submitted at this time."
        ),
        Status.OPEN: "The pot is open and pick sheets can be submitted.",
        Status.CLOSED: (
            "The pot is closed. No further pick sheet submissions are "
            "accepted at this point. It is now time to enter the winning teams."
        ),
        Status.TALLY: (
            "The pot is closed and the winning teams are known. "
            "Now it's time to tally the submissions and find out "
            "who has the most correct picks on their pick sheet."
        ),
    }

    def __str__(self):
        return self.name

    def get_tally(self):
        return (
            self.pick_sheets.annotate_correct_count()
            .annotate_tiebreaker_delta()
            .annotate_tiebreaker_delta_abs()
            .order_by("-correct_count", "tiebreaker_delta_abs")
        )

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

    @property
    def next_status_action_text(self):
        return self._next_status_action_text.get(self.next_status)

    @property
    def previous_status_action_text(self):
        return self._previous_status_action_text.get(self.previous_status)

    @property
    def status_help_text(self):
        return self._status_help_text.get(self.status)

    @property
    def pickers_list(self):
        return self.pick_sheets.all().values_list("picker", flat=True)
