from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home",),
    path("compare", views.compare, name="compare"),
    path("trend", views.trend, name="trend"),
    path("rated", views.rated, name="rated"),
    path("contact", views.contact, name="contact"),
]
