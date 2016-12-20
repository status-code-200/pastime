from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import CustomizedUser


class Event(models.Model):
    organizer = models.CharField(max_length=100, verbose_name='организатор')
    event_name = models.CharField(max_length=100, verbose_name='название мероприятия')
    event_description = models.TextField(verbose_name='описание мероприятия')
    event_status = models.CharField(max_length=8, default='open',
                                    choices=(('open', 'открытое'),
                                             ('closed', 'закрытое')),
                                    verbose_name='форма мероприятия')
    event_location = models.CharField(max_length=1000,
                                      verbose_name='месторасположение')
    event_number_of_persons = models.IntegerField(default='10',
                                                  validators=[MinValueValidator(2),
                                                              MaxValueValidator(100)],
                                                  verbose_name='количество человек')
    event_persons = models.ManyToManyField(CustomizedUser,
                                           verbose_name='уже идут',
                                           blank=True)

    def __str__(self):
        return self.event_name
