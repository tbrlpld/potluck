from django.contrib import admin

# Register your models here.
from potluck.teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
