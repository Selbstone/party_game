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
        self.first_name = user_chat['first_name']
        self.username = user_chat['username']
        self.telegram_id = user_chat['id']

        if text == '/start':
            self.start()
        elif text == '/start_game':
            self.start_game()
        elif text == '/party':
            self.party()
        else:
            send_mess(self.telegram_id, 'Пока что мой функционал очень ограничен :(')

        return HttpResponse(True)

    def start(self):
        if not UserBot.objects.filter(telegram_id=self.telegram_id).exists():
            UserBot.objects.create(
                first_name=self.first_name,
                username=self.username,
                telegram_id=self.telegram_id
            )
            send_mess(self.telegram_id, 'Поздравляю, вы участвуете в игре!')
        else:
            send_mess(self.telegram_id, 'Вы уже зарегистрированы, дождитесь других участников.')

    def start_game(self):
        if check_if_user_admin(self.username):
            send_goals_to_users()
        else:
            send_mess(self.telegram_id, 'Только админ может начать игру.')

    def party(self):
        users = UserBot.objects.all()
        party = ''
        for user in users:
            party = party + f'{str(user)}\n'
        send_mess(self.telegram_id, party)
