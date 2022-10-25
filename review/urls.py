from django.urls import path
from review import views


urlpatterns = [
    path("", views.feed, name='feed'),
    path("ticket/new/", views.create_ticket, name='create_ticket'),
    path("ticket/<int:ticket_id>/reply/", views.create_review_reply, name='create_review_reply'),
    path("review/new", views.create_review, name='create_review'),
    path("my-posts", views.posts, name='posts'),
    path("my-posts/ticket-<int:post_id>/update/", views.update_post, name='update_ticket'),
    path("my-posts/ticket-<int:post_id>/delete/", views.delete_post, name='delete_ticket'),
    path("my-posts/review-<int:post_id>/update/", views.update_post, name='update_review'),
    path("my-posts/review-<int:post_id>/delete/", views.delete_post, name='delete_review'),
    path("subscriptions/", views.subscriptions, name='subscriptions'),
]
