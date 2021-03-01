from django.contrib import admin

from potluck.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
