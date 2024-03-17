from django.urls import path
from . import views


urlpatterns = [
    path(
        "existing_machine_types/",
        views.existing_machine_types_view,
        name="existing_machine_types"
    ),
    path(
        "list_machine_types/",
        views.list_machine_types_view,
        name="list_machine_types"
    ),
    path(
        "create_machine_type/",
        views.create_machine_type_view,
        name="create_machine_type"
    ),
    path(
        "update_machine_type/",
        views.update_machine_type_view,
        name="update_machine_type"
    ),
    path(
        "delete_machine_type/<int:id>/",
        views.delete_machine_type_view,
        name="delete_machine_type"
    ),
    path(
        "list_machines/",
        views.list_machines_view,
        name="list_machines"
    ),
    path(
        "create_machine/",
        views.create_machine_view,
        name="create_machine"
    ),
    path(
        "update_machine/",
        views.update_machine_view,
        name="update_machine"
    ),
    path(
        "delete_machine/<int:id>/",
        views.delete_machine_view,
        name="delete_machine"
    ),
]

