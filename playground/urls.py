from django.urls import path
from . import views

urlpatterns = [
    path("slow/", views.slow),
]
