from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models


@login_required
def feed(r):
    tickets = models.Ticket.objects.all()
    return render(
        r,
        'review/feed.html',
        {'tickets': tickets}
    )

@login_required
def create_ticket(r):
    if r.method == 'POST':
        form = forms.TicketForm(r.POST, r.FILES)
        ticket = form.save(commit=False)
        ticket.user = r.user
        ticket.save()
        return redirect('feed')
    else:
        form = forms.TicketForm()

    return render(
        r,
        'review/create_ticket.html',
        {'form': form}
    )
