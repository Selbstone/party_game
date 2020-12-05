import json
import logging

from django.http import HttpResponse
from django.views.generic import View

from .models import UserBot
from .utils import send_mess, check_if_user_admin, send_goals_to_users

logger = logging.getLogger('bot')
logger_django = logging.getLogger('django')


class BotWebhook(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        logger_django.info(body)

        user_info = body['message']['from']
        try:
            text = body['message']['text']
            self.first_name = user_info['first_name']
            self.username = user_info['username']
            self.telegram_id = user_info['id']
        except KeyError:
            return HttpResponse(True)

        if text == '/start' or text == '/start@party_game_vg_bot':
            self.start()
        elif text == '/start_game':
            self.start_game()
        elif text == '/party' or text == '/party@party_game_vg_bot':
            self.party()
        elif text == '/leave' or text == '/leave@party_game_vg_bot':
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
