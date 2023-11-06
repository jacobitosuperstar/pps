from django.urls import path
from . import views


urlpatterns = [
    path(
        "login/",
        views.EmployeeLogInView.as_view({"post": "employee_login"}),
        name="login"
    ),
    path(
        "logout/",
        views.EmployeeLogInView.as_view({"get": "employee_logout"}),
        name="logout"
    ),
    path(
        "/",
        views.EmployeeCRUDView.as_view({"get": "get_employees"}),
        name="get_employees"
    ),
    path(
        "create/",
        views.EmployeeCRUDView.as_view({"post": "create_employee"}),
        name="create_employees"
    ),
    path(
        "<int:pk>/",
        views.EmployeeCRUDView.as_view({"get": "get_employee"}),
        name="get_employee"
    ),
    path(
        "<int:pk>/update/",
        views.EmployeeCRUDView.as_view({"put": "update_employee"}),
        name="update_employee"
    ),
    path(
        "<int:pk>/delete/",
        views.EmployeeCRUDView.as_view({"delete": "delete_employee"}),
        name="delete_employee"
    ),
]
