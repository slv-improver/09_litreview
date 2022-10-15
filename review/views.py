from django.shortcuts import render


def home(r):
    return render(
        r,
        'review/home.html'
    )
