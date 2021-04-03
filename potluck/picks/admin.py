from django.contrib import admin

from potluck.picks.models import GamePick, Pick


# Register your models here.
@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(GamePick)
class GamePickAdmin(admin.ModelAdmin):
    pass
