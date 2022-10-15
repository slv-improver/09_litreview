from django.contrib.auth import login, authenticate
from django.shortcuts import render
from . import forms


def signup(r):
    if r.method == 'POST':
        form = forms.SignupForm(r.POST)
        if form.is_valid():
            user = form.save()
            login(r, user)
    else:
        form = forms.SignupForm()
    return render(
        r,
        'authentication/signup.html',
        {'form': form}
    )

def log_user(r):
    if r.method == 'POST':
        form = forms.LoginForm(r.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(r, user)
    else:
        form = forms.LoginForm()
    return render(
        r,
        'authentication/login.html',
        {'form': form}
    )
