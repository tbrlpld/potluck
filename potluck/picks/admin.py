from django.contrib import admin

from potluck.picks.models import GamePickTemp, PickSheet


# Register your models here.
@admin.register(PickSheet)
class PickAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(GamePickTemp)
class GamePickAdmin(admin.ModelAdmin):
    pass
