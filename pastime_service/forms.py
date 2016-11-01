from django import forms
from .models import Event
from material import *
from django.core.validators import MaxValueValidator, MinValueValidator

class EventForm(forms.Form):
    organizer = forms.CharField(label='Организатор', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    event_name = forms.CharField(label='Название мероприятия')
    event_description = forms.CharField(widget=forms.Textarea,  label='Описание мероприятия')
    event_status = forms.ChoiceField(choices=(('open', 'открытое'), ('closed', 'закрытое')), label='Форма мероприятия')
    event_location = forms.CharField(max_length=1000, label='Месторасположение')

    layout = Layout(Row(Column('event_name'),
                    Column('organizer',
                            'event_description',
                            'event_location'),
                    Column('event_status')))

    def save(self):
        data = self.cleaned_data
        event = Event(organizer=data['organizer'], event_name=data['event_name'], event_description=data['event_description'], event_status=data['event_status'], event_location=data['event_location'] )
        event.save()
