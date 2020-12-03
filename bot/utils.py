import random

import requests
from django.conf import settings

from .models import UserBot


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(settings.BOT_URL + 'sendMessage', data=params)
    return response


def check_if_user_admin(username):
    return username == settings.ADMIN_USERNAME


def shuffle_users(users):
    random.shuffle(users)
    offset_list = [users[-1], *users[:-1]]
    return list(zip(users, offset_list))


def send_goals_to_users():
    users = UserBot.objects.all()
    pairs = shuffle_users(list(users))
    for pair in pairs:
        send_mess(pair[0].telegram_id, f'Ваша цель: {pair[1]}! Удачи :)')
    return True
