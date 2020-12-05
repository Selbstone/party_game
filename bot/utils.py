import logging
import random

import requests
from django.conf import settings

from .models import UserBot

logger = logging.getLogger('bot')

thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'  # Code: 300's
rain = u'\U00002614'  # Code: 500's
snowflake = u'\U00002744'  # Code: 600's snowflake
snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'  # Code: 700's foogy
clearSky = u'\U00002600'  # Code: 800 clear sky
fewClouds = u'\U000026C5'  # Code: 801 sun behind clouds
clouds = u'\U00002601'  # Code: 802-803-804 clouds general
hot = u'\U0001F525'  # Code: 904
defaultEmoji = u'\U0001F300'  # default emojis

emojies = (
    thunderstorm,
    drizzle,
    rain,
    snowflake,
    atmosphere,
    clearSky,
    fewClouds,
    clouds,
    hot,
    defaultEmoji,
)


def random_emoji():
    return random.choice(emojies)


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
    emoji = random_emoji()
    for pair in pairs:
        send_mess(pair[0].telegram_id, f'Ваша цель: {pair[1]}! Удачи :) {emoji}')
    logger.info(f'The game started. Count of participants {len(users)}')
    logger.info(f'Pairs: {pairs}')
    return True
