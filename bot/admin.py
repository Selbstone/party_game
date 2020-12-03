from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import re_path

from .models import UserBot
from .utils import send_goals_to_users


# Register your models here.
class UserBotAdmin(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"

    def get_urls(self):
        urls = super(UserBotAdmin, self).get_urls()
        custom_urls = [
            re_path('^start_game/$', self.start_game, name='start_game'),
        ]
        return custom_urls + urls

    def start_game(self, request):
        send_goals_to_users()
        self.message_user(request, f"Игра успешно началась!")
        return HttpResponseRedirect("../")


admin.site.register(UserBot, UserBotAdmin)
