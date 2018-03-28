from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm,
    SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.


def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

