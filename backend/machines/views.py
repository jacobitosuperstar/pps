from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.http import JsonResponse
from base.http_status_codes import HTTP_STATUS as status
from base.logger import base_logger

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
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def existing_machine_types_view(request: HttpRequest) -> JsonResponse:
    """List of the current machine types existing in the company. Do not
    confuse this view with the other machine type, that is where we store the
    type of machines that exists and also store the employees that are trained
    to use those types of machinery.
    """
    return JsonResponse(ExistingMachineTypes_dict)


@require_GET
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def list_machine_types_view(request: HttpRequest) -> JsonResponse:
    """List of machine types with all the employees trained to use them.
    """
    machine_types = MachineType.objects.filter(
        is_deleted=False,
    ).prefetch_related("trained_employees")

    machine_types_list = [
        machine_type.serializer(depth=1) for machine_type in machine_types
    ]
    return JsonResponse({"machine_types_list": machine_types_list})


@require_POST
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def create_machine_type_view(request: HttpRequest) -> JsonResponse:
    """Creates a new machine type on which the employees are going to be or
    are trained on.
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
        )
        machine_type.save()

        trained_employees = form.cleaned_data.get("trained_employees")
        if trained_employees:
            machine_type.trained_employees.add(*trained_employees)

        msg = {"machine_type": machine_type.serializer(depth=1)}
        return JsonResponse(msg, status=status.created)
    except Exception as e:
        raise e
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def update_machine_type_view(request: HttpRequest) -> JsonResponse:
    """Updates the given machine type. This view is used mostly to add trained
    employees to the machine type or to take them away.
    """
    form = MachineTypeForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    try:
        machine_type: MachineType = MachineType.objects.get(
            id=form.cleaned_data["id"],
        )
        changed = False

        if form.cleaned_data.get("machine_type"):
            machine_type.machine_type = form.cleaned_data["machine_type"]
            changed = True

        trained_employees_to_add = form.cleaned_data.get("trained_employees_to_add")

        if trained_employees_to_add:
            machine_type.trained_employees.add(*trained_employees_to_add)
            changed = True

        trained_employees_to_delete = form.cleaned_data.get("trained_employees_to_delete")

        if trained_employees_to_delete:
            machine_type.trained_employees.remove(*trained_employees_to_delete)
            changed = True

        if changed:
            machine_type.save()

        msg = {"machine_type": machine_type.serializer(depth=1)}
        return JsonResponse(msg, status=status.accepted)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_http_methods(["DELETE"])
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.PRODUCTION_MANAGER])
def delete_machine_type_view(request: HttpRequest, id: int) -> JsonResponse:
    """Deletes a machine type given the ID.
    """
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


@require_GET
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def list_machines_view(request: HttpRequest) -> JsonResponse:
    """List of the machines that are in the company.
    """
    machines = Machine.objects.filter(
        is_deleted=False,
    ).select_related("machine_type")

    machines_list = [
        machine.serializer(depth=1) for machine in machines
    ]
    return JsonResponse({"machines_list": machines_list})


@require_POST
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
    ]
)
def create_machine_view(request: HttpRequest) -> JsonResponse:
    """creates a new machine.
    """
    form = MachineCreationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    machine = Machine(
        machine_number=form.cleaned_data.get("machine_number"),
        machine_title=form.cleaned_data.get("machine_title"),
        machine_type=form.cleaned_data.get("machine_type"),
    )
    machine.save()
    msg = {
        "response": _("Machine created successfully"),
        "machine": machine.serializer(depth=1),
    }
    return JsonResponse(msg, status=status.created)


@require_POST
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
    ]
)
def update_machine_view(request: HttpRequest) -> JsonResponse:
    """Updates the machine with the specified ID in the given fields.
    """
    form = MachineForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    machine_number = form.cleaned_data.get("machine_number")
    machine_title = form.cleaned_data.get("machine_title")
    machine_type = form.cleaned_data.get("machine_type_id")

    try:
        machine: Machine = Machine.objects.get(
            id=form.cleaned_data["machine_id"]
        )
        changed = False

        if machine_number:
            machine.machine_number = machine_number
            changed = True
        if machine_title:
            machine.machine_title = machine_title
            changed = True
        if machine_type:
            machine.machine_type = machine_type
            changed = True

        if changed:
            machine.save()
            msg = {
                "response": _("Machine updated successfully."),
                "machine": machine.serializer(depth=0),
            }
        else:
            msg = {
                "response": _("Machine not changed."),
                "machine": machine.serializer(depth=0),
            }
        return JsonResponse(msg, status=status.accepted)
    except Machine.DoesNotExist:
        msg = {
            "response": _("Machine entry not found.")
        }
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_http_methods(["DELETE"])
@authenticated_user
@role_validation(
    allowed_roles=[
        RoleChoices.PRODUCTION_MANAGER,
    ]
)
def delete_machine_view(request: HttpRequest, id: int) -> JsonResponse:
    """Deletes the given machine from the factory.
    """
    try:
        machine: Machine = Machine.objects.get(id=id)
        machine.delete()
        msg = {
            "response": _("Machine entry deleted successfully.")
        }
        return JsonResponse(msg, status=status.accepted)
    except Machine.DoesNotExist:
        msg = {
            "response": _("Machine entry not found.")
        }
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)
