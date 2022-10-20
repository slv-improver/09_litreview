from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from . import models


@login_required
def feed(r):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(
        r,
        'review/feed.html',
        {'tickets': tickets, 'reviews': reviews}
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

@login_required
def create_review(r, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if r.method == 'POST':
        form = forms.ReviewForm(r.POST, r.FILES)
        review = form.save(commit=False)
        review.user = r.user
        review.ticket = ticket
        review.save()
        return redirect('feed')
    else:
        form = forms.ReviewForm()

    return render(
        r,
        'review/create_review.html',
        {'form': form, 'ticket': ticket}
    )
