from django.db import models


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
