from django.urls import path
from review import views


urlpatterns = [
    path("", views.feed, name='feed'),
    path("ticket/new/", views.create_ticket, name='create_ticket'),
    path("ticket/<int:ticket_id>/reply/", views.create_review, name='create_review'),
]
