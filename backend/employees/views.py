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

from .models import (
    Employee,
    RoleChoices,
    OOO,
    OOOTypes,
    RoleChoices_dict,
    OOOTypes_dict,
)
from .forms import (
    EmployeeAuthenticationForm,
    EmployeeCreationForm,
    EmployeeForm,
    OOOCreationForm,
    OOOForm,
)
from .decorators import (
    role_validation,
)


@require_GET
@authenticated_user
def employee_roles_view(request: HttpRequest) -> JsonResponse:
    """List of work roles for the different kind of employees.
    """
    return JsonResponse(RoleChoices_dict)


@require_GET
@authenticated_user
def employee_ooo_types_view(request: HttpRequest) -> JsonResponse:
    """List of work roles for the different kind of employees.
    """
    return JsonResponse(OOOTypes_dict)


@require_POST
def employee_login_view(request: HttpRequest) -> JsonResponse:
    """Logs in the employee into the platform.
    """
    form = EmployeeAuthenticationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    identification = form.cleaned_data.get("identification")
    password = form.cleaned_data.get("password")
    employee = authenticate(
        request,
        identification=identification,
        password=password
    )
    if not employee:
        msg = {
            "response": _("Invalid credentials, check the ID or the Password"),
        }
        return JsonResponse(msg, status=status.bad_request)

    token = create_token(
        employee_id=employee.id,
        employee_role=employee.role,
    )

    msg = {
        "response": _("Logged in successfully"),
        "token": token,
    }
    return JsonResponse(msg)


@require_GET
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT])
def list_employees_view(
    request: HttpRequest
) -> JsonResponse:
    """GETs the list of active employees in a stream."""
    form = EmployeeForm(request.GET)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    identification = form.cleaned_data.get("identification")
    names = form.cleaned_data.get("names")
    last_names = form.cleaned_data.get("last_names")
    birthday = form.cleaned_data.get("birthday")
    role = form.cleaned_data.get("role")
    is_active = form.cleaned_data.get("is_active", True)

    query = Q()
    if identification:
        query &= Q(identification=identification)
    if names:
        query &= Q(names=names)
    if last_names:
        query &= Q(last_names=last_names)
    if birthday:
        query &= Q(birthday=birthday)
    if role:
        query &= Q(role=role)
    if is_active:
        query &= Q(is_active=is_active)

    employees = Employee.objects.filter(query)

    employees_list = [employee.serializer() for employee in employees]
    return JsonResponse({"employess": employees_list})


@require_GET
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT,])
def get_employee_view(request: HttpRequest, cc: str) -> JsonResponse:
    """GETs the searched employee."""
    try:
        employee = Employee.objects.get(identification=cc)
        return JsonResponse(employee.serializer(), status=status.ok)
    except Employee.DoesNotExist as e:
        msg = {
            "response": _("Employee not found.")
        }
        base_logger.error(e)
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR])
def create_employee_view(request: HttpRequest) -> JsonResponse:
    """CREATES the employee."""
    form = EmployeeCreationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    if form.cleaned_data["role"] not in (RoleChoices.PRODUCTION, ""):
        password = secrets.token_urlsafe(8)
    else:
        password = None

    identification = form.cleaned_data["identification"]
    names = form.cleaned_data["names"]
    last_names = form.cleaned_data["last_names"]
    birthday = form.cleaned_data["birthday"]
    role = form.cleaned_data["role"]

    try:
        user: Employee = Employee.objects.create_user(
            identification=identification,
            names=names,
            last_names=last_names,
            birthday=birthday,
            password=password,
            role=role,
        )
        msg = {
            "identification": user.identification,
            "role": user.role,
        }
        if password:
            msg["generated_password"] = password
        return JsonResponse(msg, status=status.created)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_http_methods(["PATCH"])
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR])
def update_employee_view(request: HttpRequest, cc: str) -> JsonResponse:
    """UPDATES the employee"""
    form = EmployeeForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    return JsonResponse({})


@require_http_methods(["DELETE"])
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR])
def delete_employee_view(request: HttpRequest, cc: str) -> JsonResponse:
    """DELETES the employee"""
    try:
        employee = Employee.objects.get(identification=cc)
        employee.is_active = False
        employee.save()
        msg = {
            "response": _("Employee deactivated successfully.")
        }
        return JsonResponse(msg, status=status.accepted)
    except Employee.DoesNotExist as e:
        msg = {
            "response": _("Employee not found.")
        }
        base_logger.error(e)
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR])
def create_ooo_view(request: HttpRequest) -> JsonResponse:
    """Creates the OOO entry for the sended user."""
    form = OOOCreationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    try:
        ooo_time = OOO(
            employee=form.cleaned_data.get("employee_identification"),
            ooo_type=form.cleaned_data.get("ooo_type"),
            start_date=form.cleaned_data.get("start_date"),
            end_date=form.cleaned_data.get("end_date"),
            description=form.cleaned_data.get("description"),
        )
        ooo_time.save()
        msg = {"ooo_time": ooo_time.serializer(depth=1)}
        return JsonResponse(msg, status=status.created)
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
        RoleChoices.HR,
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
)
def list_ooo_view(request: HttpRequest) -> JsonResponse:
    """GETs the list of OOOs."""
    form = OOOForm(request.GET)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    employee = form.cleaned_data.get("employee_identification")
    ooo_type = form.cleaned_data.get("ooo_type")
    start_date = form.cleaned_data.get("start_date")
    end_date = form.cleaned_data.get("end_date")

    query = Q()
    if employee:
        query &= Q(employee=employee)
    if ooo_type:
        query &= Q(ooo_type=ooo_type)
    if start_date:
        query &= Q(start_date__gte=start_date)
    if end_date:
        query &= Q(end_date__lte=end_date)

    ooos = OOO.objects.filter(query).select_related("employee")
    ooo_list = [ooo.serializer(depth=1) for ooo in ooos]
    return JsonResponse({"ooo_list": ooo_list})


@require_http_methods(["DELETE"])
@authenticated_user
@role_validation(allowed_roles=[RoleChoices.HR])
def delete_ooo_view(request: HttpRequest, id: int) -> JsonResponse:
    try:
        ooo = OOO.objects.get(id=id)
        ooo.delete()
        msg = {
            "response": _("OOO entry deleted successfully.")
        }
        return JsonResponse(msg, status=status.accepted)
    except OOO.DoesNotExist as e:
        msg = {
            "response": _("OOO entry not found.")
        }
        base_logger.error(e)
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        base_logger.critical(e)
        return JsonResponse(msg, status=status.internal_server_error)
