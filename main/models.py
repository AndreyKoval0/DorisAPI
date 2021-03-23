from django.db import models

class Bot(models.Model):
    creater = models.CharField("Создатель", max_length=200)
    api_key = models.CharField("API ключ", max_length=200)