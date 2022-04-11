from django.contrib import admin

from django.contrib import admin

from project_prep.main.models import Garment, GarmentPhoto


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


