from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import EventForm
from .models import Event, APIKey


def logUserIn(request):
    username_or_email = request.POST['username_or_email']
    password = request.POST['password']
    user = authenticate(username=username_or_email, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            print("User is valid, active and authenticated")
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and pass
        print("The username and password were incorrect.")

    response = render(request, 'pastime_service/index.html', {})
    return response


def logUserOut(request):
    logout(request)
    return redirect('/')


def index(request):
    if request.user.is_authenticated and request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('/pastime')
    else:
        form = EventForm(initial={'organizer': request.user.username})
        events = Event.objects.all()
        try:
            key = APIKey.objects.get(key_name='google_api_maps_js')
        except APIKey.DoesNotExist:
            return render(request,
                          'pastime_service/index.html',
                          {'form': form,
                           'events': events
                           })

    return render(request, 'pastime_service/index.html', {'form': form,
                                                          'events': events,
                                                          'key': key.key
                                                          })
