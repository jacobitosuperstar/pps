from django.urls import path
from . import views


urlpatterns = [
    path("pin/", views.pin_view, name="pin"),
    path("logged_pin/", views.logged_pin_view, name="logged_pin"),
]
