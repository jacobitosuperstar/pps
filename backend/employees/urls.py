"""Machines module endpoints.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'', views.EmployeeViewSet, basename='employee')


urlpatterns = [
    path(
        "roles/",
        views.EmployeeRolesView.as_view(),
        name="employees_roles"
    ),
    path(
        "ooo_types/",
        views.EmployeeOOOTypesView.as_view(),
        name="employees_ooo_types"
    ),
    path(
        "login/",
        views.EmployeeLoginView.as_view(),
        name="employees_login"
    ),
    path(
        "filtered/",
        views.EmployessFilteredView.as_view(),
        name="employees_filtered"
    ),
    path(
        "ooo/",
        views.OOOsView.as_view(),
        name="employees_ooos"
    ),
    path(
        "ooo/filtered/",
        views.OOOsFilteredListView.as_view(),
        name="employees_filtered_ooo"
    ),
    path(
        "ooo/<int:id>",
        views.OOODUDView.as_view(),
        name="employees_dud_ooo"
    ),
    path(
        "<str:identification>/",
        views.EmployeeDUDView.as_view(),
        name="employees_dud_employee"
    ),
    path('', include(router.urls)),
]
