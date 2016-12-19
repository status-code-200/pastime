from django import forms
from .models import Event
from accounts.models import CustomizedUser
from django.http import JsonResponse
from django.views.generic.edit import FormView

from django.contrib.auth import authenticate, login
from accounts.forms import UserCreationForm

from django.core.validators import MaxValueValidator, MinValueValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Неправильный логин или пароль.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class EventForm(forms.Form):
    organizer = forms.CharField(label='Организатор', widget=forms.TextInput(attrs={'id': 'event_organizer', 'readonly':'readonly', 'class': "mdl-textfield__input"}))
    event_name = forms.CharField(label='Название мероприятия', widget=forms.TextInput(attrs={'id': 'event_name', 'class': "mdl-textfield__input"}))
    event_description = forms.CharField(widget=forms.Textarea(attrs={'id': 'event_description', 'class': "mdl-textfield__input", 'style':'resize:none;'}),  label='Описание мероприятия', help_text='100 characters max.')
    event_status = forms.ChoiceField(choices=(('open', 'открытое'), ('closed', 'закрытое')), label='Форма мероприятия', widget=forms.Select(attrs={'id': 'event_status', 'class': "mdl-textfield__input"}))
    event_location = forms.CharField(max_length=1000, label='Месторасположение', widget=forms.TextInput(attrs={'id': 'event_location', 'readonly':'readonly', 'class': "mdl-textfield__input"}))
    event_number_of_persons = forms.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(100)], label='количество человек', widget=forms.TextInput(attrs={'type':'number', 'id': 'event_number_of_persons', 'class': "mdl-textfield__input"}))

    def save(self):
        data = self.cleaned_data
        event = Event(**data)
        event.save()


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'id': 'registration_username', 'class': "mdl-textfield__input"}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'id': 'registration_email', 'class': "mdl-textfield__input"}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'registration_password1', 'class': "mdl-textfield__input"}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'registration_password2', 'class': "mdl-textfield__input"}), label="Password (again)")

    class Meta:
        model = CustomizedUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        try:
            user = CustomizedUser.objects.get(username__iexact=self.cleaned_data['username'])
        except CustomizedUser.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("The username already exists. Please try another one.")

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email').lower()
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        if self.request.is_ajax():
            error_message = dict([(key, [error for error in value]) for key, value in form.errors.items()])
            return JsonResponse(error_message, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        if 'registration' in self.template_name:
            username = self.request.POST.get('username')
            password = self.request.POST.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
        if self.request.is_ajax():
            return JsonResponse({}, status=200)
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)


class EventFormTemplate(AjaxableResponseMixin, FormView):
    template_name = 'pastime_service/event.html'
    form_class = EventForm
    success_url = '/'


class RegistrationFormTemplate(AjaxableResponseMixin, FormView):
    template_name = 'pastime_service/registration.html'
    form_class = RegistrationForm
    success_url = '/'
