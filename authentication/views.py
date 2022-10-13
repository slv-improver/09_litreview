from django.shortcuts import render


def signup(r):
    return render(
        r,
        'authentication/signup.html',
    )
