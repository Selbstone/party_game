import json
import logging

from django.http import HttpResponse
from django.views.generic import View

from .models import UserBot
from .utils import send_mess, check_if_user_admin, send_goals_to_users

logger = logging.getLogger(__name__)


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
        elif text == '/start_game':
            if check_if_user_admin(username):
                send_goals_to_users()
            else:
                send_mess(telegram_id, 'Только админ может начать игру.')
        elif text == '/party':
            users = UserBot.objects.all()
            party = ''
            for user in users:
                party = party + f'{str(user)}\n'
            send_mess(telegram_id, party)
        else:
            send_mess(telegram_id, 'Пока что мой функционал очень ограничен :(')

        return HttpResponse(True)
