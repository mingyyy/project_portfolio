from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session

def register(request):
    '''REgister a new user.'''
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('app_port:main'))
    context = {'form':form}
    return render(request, 'register.html', context)


def logout_view(request):
    '''log the user out.'''
    # session_key = request.data['sessionKey']
    # session = Session.objects.get(session_key=session_key)
    # Session.objects.filter(session_key=session).delete()
    # Session.objects.all().delete()

    logout(request)
    return HttpResponseRedirect(reverse('app_port:main'))