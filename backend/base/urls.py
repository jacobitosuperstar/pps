from django.urls import path, re_path
from . import views


urlpatterns = [
    path("pin/", views.pin_view, name="pin"),
    path("logged_pin/", views.logged_pin_view, name="logged_pin"),
    # re_path(r'^.*$', views.ReactAppView.as_view(), name='react-app'),
]
