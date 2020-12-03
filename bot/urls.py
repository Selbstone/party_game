from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BotWebhook

urlpatterns = [
    path(f'{settings.TOKEN}', csrf_exempt(BotWebhook.as_view())),
]
