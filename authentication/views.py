from django.shortcuts import render
from . import forms


def signup(r):
    if r.method == 'POST':
        form = forms.SignupForm(r.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = forms.SignupForm()
    return render(
        r,
        'authentication/signup.html',
        {'form': form}
    )
