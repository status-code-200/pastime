from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import EventForm, LoginForm
from .models import Event
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

@login_required
def join_event(request):
    if request.method == 'POST':
        print(dir(request))
        print(request.user.id)
    return JsonResponse({})


def logUserIn(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('/')
        else:
            error_message = dict([(key, [error for error in value]) for key, value in form.errors.items()])
            return JsonResponse(error_message, status=400)
    return redirect('/')

def logUserOut(request):
    logout(request)
    return redirect('/')

def index(request):
    event_form = EventForm(initial={'organizer': request.user.username})
    registration_form = RegistrationForm()
    events = Event.objects.all()
    return render(request, 'pastime_service/index.html', {'form': event_form, 'events': events, 'registration_form': registration_form})
