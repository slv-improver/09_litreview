from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from itertools import chain
from . import forms
from . import models


@login_required
def feed(r):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    posts = sorted(
        chain(tickets,reviews), 
        key=lambda x: x.time_created, 
        reverse=True
    )
    return render(
        r,
        'review/feed.html',
        {'posts': posts}
    )

@login_required
def create_ticket(r):
    if r.method == 'POST':
        form = forms.TicketForm(r.POST, r.FILES)
        if form.is_valid():
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
def create_review_reply(r, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if r.method == 'POST':
        form = forms.ReviewForm(r.POST, r.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = r.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        form = forms.ReviewForm()

    return render(
        r,
        'review/create_review_reply.html',
        {'form': form, 'ticket': ticket}
    )

@login_required
def create_review(r):
    if r.method == 'POST':
        ticket_form = forms.TicketForm(r.POST, r.FILES)
        review_form = forms.ReviewForm(r.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = r.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = r.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    return render(
        r,
        'review/create_review.html',
        {'ticket_form': ticket_form, 'review_form': review_form}
    )

@login_required
def posts(r):
    tickets = models.Ticket.objects.filter(user=r.user)
    reviews =  models.Review.objects.filter(user=r.user)
    posts = sorted(
        chain(tickets,reviews), 
        key=lambda x: x.time_created, 
        reverse=True
    )
    return render(
        r,
        'review/posts.html',
        {'posts': posts}
    )

@login_required
def update_ticket(r, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if r.method == 'POST':
        form = forms.TicketForm(r.POST, r.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = forms.TicketForm(instance=ticket)
    return render(
        r,
        'review/update_post.html',
        {'form': form}
    )

@login_required
def update_review(r, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if r.method == 'POST':
        form = forms.ReviewForm(r.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = forms.ReviewForm(instance=review)
    return render(
        r,
        'review/update_post.html',
        {'form': form}
    )
