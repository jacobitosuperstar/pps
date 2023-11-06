import secrets
import json
from django.shortcuts import render
from django.http import (
    HttpRequest,
    JsonResponse,
    FileResponse,
    StreamingHttpResponse,
)
from django.views import View
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
# from django.views.decorators.csrf import (
#     csrf_exempt,
#     ensure_csrf_cookie,
# )
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.http import JsonResponse
from base.http_status_codes import HTTP_STATUS
from .models import (
    Employee,
    RoleChoices,
)
from .forms import (
    EmployeeAuthenticationForm,
    EmployeeCreationForm,
    EmployeeForm,
)
from .decorators import (
    role_validation,
)


class EmployeeLogInView(View):
    @require_POST
    def employee_login(self,request: HttpRequest) -> JsonResponse:
        """Logs in the employee into the platform.
        """
        form = EmployeeAuthenticationForm(request.POST)

        if not form.is_valid():
            msg = {"response": _("Error in the information given"), }
            return JsonResponse(msg, status=HTTP_STATUS.bad_request)

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
            return JsonResponse(msg, status=HTTP_STATUS.bad_request)

        login(request, employee)
        return JsonResponse({})

    @require_GET
    def employee_logout(self, request: HttpRequest) -> JsonResponse:
        logout(request)
        return JsonResponse({})


@method_decorator(login_required, name="dispatch")
class EmployeeCRUDView(View):
    model = Employee

    @require_GET
    @role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT])
    def get_employees(self, request: HttpRequest) -> StreamingHttpResponse:
        """GETs the list of active employees in a stream."""
        queryset = Employee.objects.filter(is_active=True)
        # queryset = self.model.objects.all()
        form = EmployeeForm(request.GET)

        identification = form.cleaned_data.get("identification")
        names = form.cleaned_data.get("names")
        last_names = form.cleaned_data.get("last_names")
        birthday = form.cleaned_data.get("birthday")
        role = form.cleaned_data.get("role")
        # is_active = form.cleaned_data.get("is_active")

        if identification:
            queryset = queryset.objects.filter(identification=identification)
        if names:
            queryset = queryset.objects.filter(names=names)
        if last_names:
            queryset = queryset.objects.filter(last_names=last_names)
        if birthday:
            queryset = queryset.objects.filter(birthday=birthday)
        if role:
            queryset = queryset.objects.filter(role=role)

        def employee_stream():
            """Streams the list of employees."""
            for employee in queryset:
                employee_dict = {
                    "id": employee.id,
                    "identification": employee.identification,
                    "names": employee.names,
                    "last_names": employee.last_names,
                    "birthday": employee.birthday,
                    "role": employee.role,
                }
                yield json.dumps(employee_dict)
        response = StreamingHttpResponse(employee_stream())
        return response

    @require_POST
    @role_validation(allowed_roles=[RoleChoices.HR])
    def create_employee(self, request):
        """CREATES the employee."""

        form = EmployeeCreationForm(request.POST)

        if not form.is_valid():
            msg = {"response": _("Error in the information given"), }
            return JsonResponse(msg, status=HTTP_STATUS.bad_request)

        if form.cleaned_data["role"] != RoleChoices.PRODUCTION:
            password = secrets.token_urlsafe(8)
        else:
            password = None

        user: Employee = self.model.objects.create_user(
            identification=form.cleaned_data["identification"],
            names=form.cleaned_data["names"],
            last_names=form.cleaned_data["last_names"],
            birthday=form.cleaned_data["birthday"]
            password=password,
            role=form.cleaned_data["role"],
        )
        msg = {
            "identification": user.identification,
            "role": user.role,
        }
        if password:
            msg["generated_password"] = password
        return JsonResponse(msg, status=HTTP_STATUS.created)

    @role_validation(allowed_roles=[RoleChoices.HR, RoleChoices.MANAGEMENT,])
    def get_employee(self, request: HttpRequest, pk: int) -> JsonResponse:
        """GETs the searched employee."""
        try:
            employee = self.model.objects.get(id=pk)
            msg = {
                "id": employee.id,
                "identification": employee.identification,
                "names": employee.names,
                "last_names": employee.last_names,
                "birthday": employee.birthday,
                "role": employee.role,
            }
            return JsonResponse(msg, status=HTTP_STATUS.accepted)
        except self.model.DoesNotExists:
            msg = {
                "response": _("Employee not found.")
            }
            return JsonResponse(msg, status=HTTP_STATUS.not_found)
        except Exception as e:
            msg = {
                "response": _("Internal server error.")
            }
            return JsonResponse(msg, status=HTTP_STATUS.internal_server_error)

    @require_POST
    @role_validation(allowed_roles=[RoleChoices.HR])
    def update_employee(self, request: HttpRequest, pk: int) -> JsonResponse:
        """UPDATES the employee"""
        form = EmployeeForm(request.POST)
        return JsonResponse({})

    @role_validation(allowed_roles=[RoleChoices.HR])
    def delete_employee(self, request: HttpRequest, pk: int) -> JsonResponse:
        """DELTES the employee"""
        try:
            employee = self.model.objects.get(id=pk)
            employee.is_active = False
            employee.save()
            msg = {
                "response": _("Employee deactivated successfully.")
            }
            return JsonResponse(msg, status=HTTP_STATUS.accepted)
        except self.model.DoesNotExists:
            msg = {
                "response": _("Employee not found.")
            }
            return JsonResponse(msg, status=HTTP_STATUS.not_found)
        except Exception as e:
            msg = {
                "response": _("Internal server error.")
            }
            return JsonResponse(msg, status=HTTP_STATUS.internal_server_error)
