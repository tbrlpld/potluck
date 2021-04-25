from django.db import models


class Pot(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_tally(self):
        picks = self.picks.all()
        picks = sorted(picks, key=lambda pick: pick.count_correct(), reverse=True)
        return picks
