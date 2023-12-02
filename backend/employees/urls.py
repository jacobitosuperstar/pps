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
        "create/",
        views.create_employee_view,
        name="create_employee"
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
