from django.contrib import admin

from .models import UserBot


# Register your models here.
class UserBotAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserBot, UserBotAdmin)
