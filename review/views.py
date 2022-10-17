from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feed(r):
    return render(
        r,
        'review/feed.html'
    )
