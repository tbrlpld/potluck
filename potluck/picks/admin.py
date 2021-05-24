from django.contrib import admin

from potluck.picks.models import Pick, PickSheet


# Register your models here.
@admin.register(PickSheet)
class PickSheetAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(Pick)
class GamePickAdmin(admin.ModelAdmin):
    pass
