from django.contrib import admin

from potluck.picks.models import GamePick

# Register your models here.
@admin.register(GamePick)
class GamePickAdmin(admin.ModelAdmin):
    pass
