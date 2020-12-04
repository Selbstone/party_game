import json
import logging

from django.http import HttpResponse
from django.views.generic import View

from .models import UserBot
from .utils import send_mess, check_if_user_admin, send_goals_to_users

logger = logging.getLogger('bot')


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
        elif text == '/leave':
            self.leave()
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
            logger.info(f'{self.first_name} {self.username} join the game.')
        else:
            send_mess(self.telegram_id, 'Вы уже зарегистрированы, дождитесь других участников.')
            logger.info(f'{self.first_name} {self.username} try join the game again.')

    def start_game(self):
        if check_if_user_admin(self.username):
            send_goals_to_users()
            logger.info(f'{self.first_name} {self.username} start game.')
        else:
            send_mess(self.telegram_id, 'Только админ может начать игру.')
            logger.info(f'{self.first_name} {self.username} try start game.')

    def party(self):
        users = UserBot.objects.all()
        party = ''
        for i, user in enumerate(users, 1):
            party = party + f'{i}. {str(user)}\n'

        if party:
            send_mess(self.telegram_id, party)
        else:
            send_mess(self.telegram_id, 'Еще нет участников.')

        logger.info(f'{self.first_name} {self.username} use party command.')

    def leave(self):
        user = UserBot.objects.filter(telegram_id=self.telegram_id)
        if user:
            user.delete()
            send_mess(self.telegram_id, 'Вы покинули игру.')
            logger.info(f'{self.first_name} {self.username} leave the game.')
        else:
            send_mess(self.telegram_id, 'Вы не участвуете в игре')
            logger.info(f'{self.first_name} {self.username} try to leave the game.')
