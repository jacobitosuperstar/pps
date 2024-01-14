from typing import Union
import secrets
import json
from django.http import (
    HttpRequest,
    JsonResponse,
    StreamingHttpResponse,
)
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse
from base.http_status_codes import HTTP_STATUS as status
from base.logger import base_logger

from jwt_authentication.jwt_authentication import create_token
from jwt_authentication.decorators import authenticated_user

from employees.models import RoleChoices
from employees.decorators import (
    role_validation,
)

from .models import (
    ExistingMachineTypes_dict,
    MachineType,
    Machine,
)

from .forms import (
    MachineTypeCreationForm,
    MachineTypeForm,
    MachineCreationForm,
    MachineForm,
)


@require_GET
@authenticated_user
def existing_machine_types_view(request: HttpRequest) -> JsonResponse:
    """List of the current machine types existing in the company. Do not
    confuse this view with the other machine type, that is where we store the
    type of machines that exists and also store the employees that are trained
    to use those types of machinery.
    """
    return JsonResponse(ExistingMachineTypes_dict)


@require_GET
@authenticated_user
@role_validation(allowed_roles=[
    RoleChoices.PRODUCTION_MANAGER,
    RoleChoices.MANAGEMENT,
])
def list_machine_types_view(request: HttpRequest) -> JsonResponse:
    """List of machine types with all the employees trained to use them.
    """
    machine_types = MachineType.objects.filter(
        deleted=False,
    ).prefetch_related("trained_employees")

    machine_types_list = [
        machine_type.serializer() for machine_type in machine_types
    ]
    return JsonResponse({"machine_types_list": machine_types_list})


@require_POST
@authenticated_user
@role_validation(allowed_roles=[
    RoleChoices.PRODUCTION_MANAGER,
    RoleChoices.MANAGEMENT,
])
def create_machine_type_view(request: HttpRequest) -> JsonResponse:
    """List of machine types with all the employees trained to use them.
    """
    form = MachineTypeCreationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    try:
        machine_type = MachineType(
            machine_type=form.cleaned_data.get("machine_type"),
            trained_employees=form.cleaned_data.get("trained_employees"),
        )
        machine_type.save()
        msg = {"machine_type": machine_type.serializer()}
        return JsonResponse(msg, status=status.created)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@authenticated_user
@role_validation(allowed_roles=[
    RoleChoices.PRODUCTION_MANAGER,
    RoleChoices.MANAGEMENT,
])
def update_machine_type_view(request: HttpRequest) -> JsonResponse:
    """Updates the given machine type. This view is used mostly to add trained
    employees to the machine type.
    """
    form = MachineTypeForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    try:
        machine_type = MachineType.objects.get(
            id=form.cleaned_data["id"],
        )
        changed = False

        if form.cleaned_data.get("machine_type"):
            machine_type.machine_type = form.cleaned_data.get("machine_type")
            changed = True

        trained_employees_to_add = form.cleaned_data.get("trained_employees_to_add")

        if trained_employees_to_add:
            for employee in trained_employees_to_add:
                machine_type.trained_employees.add(employee)
            changed = True

        trained_employees_to_delete = form.cleaned_data.get("trained_employees_to_delete")

        if trained_employees_to_delete:
            for employee in trained_employees_to_delete:
                machine_type.trained_employees.remove(employee)
            changed = True

        if changed:
            machine_type.save()

        msg = {"machine_type": machine_type.serializer()}
        return JsonResponse(msg, status=status.accepted)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_http_methods(["DELETE"])
@authenticated_user
@role_validation(allowed_roles=[
    RoleChoices.PRODUCTION_MANAGER,
    RoleChoices.MANAGEMENT,
])
def delete_machine_type_view(request: HttpRequest, id: int) -> JsonResponse:
    try:
        machine_type = MachineType.objects.get(id=id)
        machine_type.delete()
        msg = {
            "response": _("Machine Type entry deleted successfully.")
        }
        return JsonResponse(msg, status=status.accepted)
    except MachineType.DoesNotExist:
        msg = {
            "response": _("Machine Type entry not found.")
        }
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)
