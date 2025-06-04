"""Machines module endpoints.
"""
from django.urls import path
from . import views


urlpatterns = [
    path(
        "roles/",
        views.EmployeeRolesView.as_view(),
        name="employees_roles"
    ),
    path(
        "ooo_types/",
        views.employee_ooo_types_view,
        name="employees_ooo_types"
    ),
    path(
        "login/",
        views.EmployeeLoginView.as_view(),
        name="employees_login"
    ),
    path(
        "",
        views.EmployessView.as_view(),
        name="employees"
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
]
