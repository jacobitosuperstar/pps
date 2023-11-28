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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from base.http_status_codes import HTTP_STATUS as status
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
)
from .decorators import (
    role_validation,
)


@require_GET
def employee_roles_view(request: HttpRequest) -> JsonResponse:
    """List of work roles for the different kind of employees.
    """
    return JsonResponse(RoleChoices_dict)


@require_GET
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

    login(request, employee)
    msg = {"response": _("Logged in successfully")}
    return JsonResponse(msg)


@require_GET
@login_required
def employee_logout_view(request: HttpRequest) -> JsonResponse:
    logout(request)
    msg = {"response": _("Logged out successfully")}
    return JsonResponse(msg)


@require_GET
@login_required
@role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT])
def list_employees_view(
    request: HttpRequest
) -> Union[JsonResponse, StreamingHttpResponse]:
    """GETs the list of active employees in a stream."""
    form = EmployeeForm(request.GET)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
        }
        return JsonResponse(msg, status=status.bad_request)

    identification = form.cleaned_data.get("identification")
    names = form.cleaned_data.get("names")
    last_names = form.cleaned_data.get("last_names")
    birthday = form.cleaned_data.get("birthday")
    role = form.cleaned_data.get("role")
    is_active = form.cleaned_data.get("is_active", True)

    employees = Employee.objects.all()
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

    def employee_stream():
        """Streams the list of employees."""
        for employee in employees:
            yield json.dumps(employee.serializer())
    response = StreamingHttpResponse(employee_stream(), status=status.ok)
    return response


@require_GET
@login_required
@role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT,])
def get_employee_view(request: HttpRequest, cc: str) -> JsonResponse:
    """GETs the searched employee."""
    try:
        employee = Employee.objects.get(identification=cc)
        return JsonResponse(employee.serializer(), status=status.ok)
    except Employee.DoesNotExist:
        msg = {
            "response": _("Employee not found.")
        }
        return JsonResponse(msg, status=status.not_found)
    except Exception as e:
        msg = {
            "response": _("Internal server error.")
        }
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@login_required
@role_validation(allowed_roles=[RoleChoices.HR])
def create_employee_view(request: HttpRequest) -> JsonResponse:
    """CREATES the employee."""
    form = EmployeeCreationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors
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


@require_http_methods(["PATCH"])
@login_required
@role_validation(allowed_roles=[RoleChoices.HR])
def update_employee_view(request: HttpRequest, cc: str) -> JsonResponse:
    """UPDATES the employee"""
    form = EmployeeForm(request.POST)

    if not form.is_valid():
        msg = {"response": _("Error in the information given"), }
        return JsonResponse(msg, status=status.bad_request)

    return JsonResponse({})


@require_http_methods(["DELETE"])
@login_required
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
    except Employee.DoesNotExist:
        msg = {
            "response": _("Employee not found.")
        }
        return JsonResponse(msg, status=status.not_found)
    except Exception:
        msg = {
            "response": _("Internal server error.")
        }
        return JsonResponse(msg, status=status.internal_server_error)


@require_POST
@login_required
@role_validation(allowed_roles=[RoleChoices.HR])
def create_ooo_view(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})
