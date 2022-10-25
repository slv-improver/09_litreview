from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from itertools import chain
from . import forms
from . import models
from authentication import models as auth_models


@login_required
def feed(r):
    followed_users = auth_models.UserFollows.objects.filter(
        user=r.user
    ).values_list('followed_user')
    tickets = models.Ticket.objects.filter(user_id__in=followed_users)
    reviews = models.Review.objects.filter(user_id__in=followed_users)
    print(tickets)
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
def update_post(r, post_id):
    if 'ticket' in r.path:
        post = get_object_or_404(models.Ticket, id=post_id)
    elif 'review' in r.path:
        post = get_object_or_404(models.Review, id=post_id)
    if r.method == 'POST':
        if 'ticket' in r.path:
            form = forms.TicketForm(r.POST, r.FILES, instance=post)
        elif 'review' in r.path:
            form = forms.ReviewForm(r.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        if 'ticket' in r.path:
            form = forms.TicketForm(instance=post)
        elif 'review' in r.path:
            form = forms.ReviewForm(instance=post)
    return render(
        r,
        'review/update_post.html',
        {'form': form}
    )

@login_required
def delete_post(r, post_id):
    if 'ticket' in r.path:
        post = get_object_or_404(models.Ticket, id=post_id)
    elif 'review' in r.path:
        post = get_object_or_404(models.Review, id=post_id)
    if r.method == 'POST':
        form = forms.DeletePostForm(r.POST)
        if form.is_valid():
            post.delete()
            return redirect('posts')
    else:
        form = forms.DeletePostForm()
    return render(
        r,
        'review/delete_post.html',
        {'form': form, 'post': post}
    )

@login_required
def subscriptions(r):
    User = get_user_model()
    if r.method == 'POST':
        form = forms.FollowUsersForm(r.POST)
        try:
            followed_user = User.objects.get(username=r.POST['followed_user'])
            if form.is_valid():
                following = auth_models.UserFollows(
                    user=r.user,
                    followed_user=followed_user
                )
                following.save()
                return redirect('subscriptions')
        except ObjectDoesNotExist:
            messages.error(r, 'The user does not exist')
        except IntegrityError:
            messages.error(r, 'You already follow this user')
    else:
        form = forms.FollowUsersForm()

    followings = auth_models.UserFollows.objects.filter(
        user=r.user
    )
    followers = auth_models.UserFollows.objects.filter(
        followed_user=r.user
    )
    return render(
        r,
        'review/subscriptions.html',
        {'form': form, 'followings': followings, 'followers': followers}
    )
