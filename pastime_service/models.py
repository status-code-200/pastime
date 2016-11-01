from django.db import models

class Event(models.Model):
    organizer = models.CharField(max_length=100, verbose_name='организатор')
    event_name = models.CharField(max_length=100, verbose_name='название мероприятия')
    event_description = models.TextField(verbose_name='описание мероприятия')
    event_status = models.CharField(max_length=8, default = 'open', choices=(('open', 'открытое'), ('closed', 'закрытое')), verbose_name='форма мероприятия')
    event_location = models.CharField(max_length=1000, verbose_name='месторасположение')

    def __str__(self):
        return self.event_name

class APIKey(models.Model):
    key_name = models.CharField(max_length=20, verbose_name='обозначение ключа')
    key = models.CharField(max_length=40, verbose_name='ключ')
    key_description = models.TextField(verbose_name='описание ключа')

    def __str__(self):
        return self.key_description
