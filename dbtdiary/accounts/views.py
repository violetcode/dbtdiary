from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import cache

from .forms import UserCreationForm

def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not "
                                "allowing new registrations.")
        return HttpResponseRedirect(reverse('aggregator:index'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('diary:index'))
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'registration/registration_form.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('diary:index'))