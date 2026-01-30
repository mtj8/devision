from django.urls import path
from . import views

urlpatterns = [
    path("match/queue", views.match_queue),
    path("match/like", views.match_like),
    path("match/pass", views.match_pass),
]