from django.contrib import admin

from potluck.picks.models import GamePickTemp, Pick


# Register your models here.
@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(GamePickTemp)
class GamePickAdmin(admin.ModelAdmin):
    pass
