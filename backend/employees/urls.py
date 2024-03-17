"""Machines module endpoints.
"""
from django.urls import path
from . import views


urlpatterns = [
    path(
        "roles/",
        views.employee_roles_view,
        name="roles"
    ),
    path(
        "ooo_types/",
        views.employee_ooo_types_view,
        name="ooo_types"
    ),
    path(
        "login/",
        views.employee_login_view,
        name="login"
    ),
    path(
        "",
        views.list_employees_view,
        name="list_employees"
    ),
    path(
        "",
        views.list_production_employees_view,
        name="list_production_employees"
    ),
    path(
        "create_employee/",
        views.create_employee_view,
        name="create_employee"
    ),
    path(
        "create_ooo/",
        views.create_ooo_view,
        name="create_ooo"
    ),
    path(
        "list_ooo/",
        views.list_ooo_view,
        name="list_ooo"
    ),
    path(
        "delete_ooo/<int:id>",
        views.delete_ooo_view,
        name="delete_ooo"
    ),
    path(
        "<str:cc>/",
        views.get_employee_view,
        name="get_employee"
    ),
    path(
        "<str:cc>/update/",
        views.update_employee_view,
        name="update_employee"
    ),
    path(
        "<str:cc>/delete/",
        views.delete_employee_view,
        name="delete_employee"
    ),
]
