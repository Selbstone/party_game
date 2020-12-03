import random


def shuffle_users(users):
    random.shuffle(users)
    offset_list = [users[-1], *users[:-1]]
    return list(zip(users, offset_list))
