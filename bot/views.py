import json

from django.http import HttpResponse
from django.views.generic import View

from .models import UserBot


class BotWebhook(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        user_chat = body['message']['chat']
        first_name = user_chat['first_name']
        username = user_chat['username']
        telegram_id = user_chat['id']

        if not UserBot.objects.filter(telegram_id=telegram_id).exists():
            UserBot.objects.create(
                first_name=first_name,
                username=username,
                telegram_id=telegram_id
            )

        return HttpResponse(True)
