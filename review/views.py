from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms


@login_required
def feed(r):
    return render(
        r,
        'review/feed.html'
    )

@login_required
def create_ticket(r):
    if r.method == 'POST':
        form = forms.TicketForm(r.POST)
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
