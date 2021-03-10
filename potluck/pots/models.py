from django.db import models


class Pot(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
