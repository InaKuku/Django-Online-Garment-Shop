from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from project_prep.accounts.models import Profile, AppUser
from project_prep.main.models import GarmentPhoto

admin.site.register(get_user_model(),)
admin.site.register(GarmentPhoto,)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')




