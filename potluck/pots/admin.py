from django.contrib import admin

from potluck.pots.models import Pot

# Register your models here.
@admin.register(Pot)
class PotAdmin(admin.ModelAdmin):
    pass
