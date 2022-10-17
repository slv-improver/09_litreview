from django.urls import path
from review import views


urlpatterns = [
    path("", views.feed, name='feed'),
    path("new-ticket/", views.create_ticket, name='create_ticket'),
]
