"""Products endpoints.
"""
from django.urls import path
from employees.models import RoleChoices
from . import views


urlpatterns = [
    path(
        "",
        views.ProductView.as_view(),
        name="products"
    ),
    path(
        "filtered/",
        views.ProductFilteredView.as_view(),
        name="products_filtered"
    ),
    path(
        "<int:id>/",
        views.ProductDUDView.as_view(),
        name="products_dud"
    ),
]
