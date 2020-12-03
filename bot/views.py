import json

import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

from .models import UserBot
from .utils import shuffle_users


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(settings.BOT_URL + 'sendMessage', data=params)
    return response


def check_if_user_admin(username):
    return username == 'iselbst'


class BotWebhook(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        user_chat = body['message']['chat']
        text = body['message']['text']
        first_name = user_chat['first_name']
        username = user_chat['username']
        telegram_id = user_chat['id']

        if text == '/start':
            if not UserBot.objects.filter(telegram_id=telegram_id).exists():
                UserBot.objects.create(
                    first_name=first_name,
                    username=username,
                    telegram_id=telegram_id
                )
                send_mess(telegram_id, 'Поздравляю, вы участвуете в игре!')
            else:
                send_mess(telegram_id, 'Вы уже зарегистрированы, дождитесь других участников.')
        elif text == '/start_game' and check_if_user_admin(username):
            users = UserBot.objects.all()
            pairs = shuffle_users(list(users))
            for pair in pairs:
                send_mess(pair[0].telegram_id, f'Твоя цель: {pair[1]}! Удачи :)')
        else:
            send_mess(telegram_id, 'Пока что мой функционал очень ограничен :(')

        return HttpResponse(True)
