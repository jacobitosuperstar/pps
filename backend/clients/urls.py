"""Clients endpoints.
"""
from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.ClientView.as_view(),
        name="clients"
    ),
    path(
        "filtered/",
        views.ClientFilteredView.as_view(),
        name="clients_filtered"
    ),
    path(
        "<str:client_id>/",
        views.ClientDUDView.as_view(),
        name="clients_dud"
    ),
]
