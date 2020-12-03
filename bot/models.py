from django.db import models


# Create your models here.


class UserBot(models.Model):
    first_name = models.CharField(max_length=32, null=True)
    username = models.CharField(max_length=32, null=True)
    telegram_id = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.username}'
