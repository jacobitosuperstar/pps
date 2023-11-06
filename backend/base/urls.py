from django.urls import path
from . import views


urlpatterns = [
    path("pin/", views.pin_view, name="pin"),
]
