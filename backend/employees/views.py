from typing import Optional
import secrets
from django.http import (
    HttpRequest,
)
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.contrib.auth import authenticate
from django.forms import ValidationError

from base.response import ORJsonResponse as JsonResponse
from base.http_status_codes import HTTP_STATUS as status
from base.logger import base_logger
from base.generic_views import (
    BaseListView,
    BaseFileteredListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

from jwt_authentication.jwt_authentication import create_token
from jwt_authentication.decorators import authenticated_user

from .decorators import role_validation
from .mixins import (
    RoleValidatorMixin,
)

from .models import (
    Employee,
    RoleChoices,
    OOO,
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


@require_GET
@authenticated_user
def employee_roles_view(request: HttpRequest) -> JsonResponse:
    """List of work roles for the different kind of employees.
    """
    return JsonResponse(RoleChoices_dict)


@require_POST
def employee_login_view(request: HttpRequest) -> JsonResponse:
    """Logs in the employee into the platform.
    """
    form: EmployeeAuthenticationForm = EmployeeAuthenticationForm(request.POST)

    if not form.is_valid():
        msg = {
            "response": _("Error in the information given"),
            "errors": form.errors,
        }
        return JsonResponse(msg, status=status.bad_request)

    identification = form.cleaned_data.get("identification")
    password = form.cleaned_data.get("password")
    employee: Optional[Employee] = authenticate(
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
        "employee": employee.serializer(depth=0),
        "token": token,
    }
    return JsonResponse(msg)


class EmployessView(
    RoleValidatorMixin,
    BaseListView
):
    """Class View to get all of the employees and for
    the creation of the employees.
    """
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.MANAGEMENT,
    ]
    model = Employee
    form: type[EmployeeCreationForm] = EmployeeCreationForm
    # serializer_depth: int = 0

    method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """CREATES the employee."""
        form = self.validate_form(request=request)

        password = None
        if form.get("role") not in (RoleChoices.PRODUCTION, ""):
            password = secrets.token_urlsafe(8)

        try:
            user: Employee = Employee.objects.create_user(**form)
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


class EmployessFilteredView(
    RoleValidatorMixin,
    BaseFileteredListView
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.MANAGEMENT,
    ]
    model = Employee
    form: type[EmployeeForm] = EmployeeForm
    serializer_depth: int = 0


class EmployeeDUDView(
    RoleValidatorMixin,
    BaseDetailView,
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.MANAGEMENT,
    ]
    model = Employee
    form = EmployeeForm
    serializer_depth = 0
    url_kwarg = "identification"

    method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """UPDATES the employee."""
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            employee = self.get_query(data=data)
            form = self.validate_form(request=request)

            form["password"] = None
            if form["role"] not in (RoleChoices.PRODUCTION, ""):
                form["password"] = secrets.token_urlsafe(8)
            employee = self.update_object(db_object=employee, data=form)
            msg = {
                "identification": employee.identification,
                "role": employee.role,
            }
            if form["password"]:
                msg["generated_password"] = form["password"]
            return JsonResponse(msg, status=status.accepted)
        except ValidationError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.bad_request)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)

    method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def delete(self, request: HttpRequest, *args, **kwargs):
        """DELETES the employee."""
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            employee = self.get_query(data=data)
            employee.is_active = False
            employee.is_deleted = True
            employee.save()
            msg = {
                "response": _(f"{self.model._meta.verbose_name} has been deleted.")
            }
            return JsonResponse(msg, status=status.accepted)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


@require_GET
@authenticated_user
def employee_ooo_types_view(request: HttpRequest) -> JsonResponse:
    """List of work roles for the different kind of employees.
    """
    return JsonResponse(OOOTypes_dict)


class OOOsView(
    RoleValidatorMixin,
    BaseListView,
    BaseCreateView,
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
    model = OOO
    form: type[OOOCreationForm] = OOOCreationForm
    prefetch_fields = []
    select_fields = ["employee"]
    serializer_depth: int = 1

    @method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def post(self, request: HttpRequest, *args, **kwargs):
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Creation of the OOO.
        """
        return super().post(request, *args, **kwargs)


class OOOsFilteredListView(
    RoleValidatorMixin,
    BaseFileteredListView,
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
    model = OOO
    form = OOOForm
    prefetch_fields = []
    select_fields = ["employee"]
    serializer_depth = 1


class OOODUDView(
    RoleValidatorMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.PRODUCTION_MANAGER,
        RoleChoices.MANAGEMENT,
    ]
    model = OOO
    form = OOOForm
    prefetch_fields = []
    select_fields = ["employee"]
    serializer_depth = 1
    url_kwarg = "id"

    @method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def post(self, request: HttpRequest, *args, **kwargs):
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Update of the OOO.
        """
        return super().post(request, *args, **kwargs)

    @method_decorator(decorator=role_validation(allowed_roles=[RoleChoices.HR]))
    def delete(self, request: HttpRequest, *args, **kwargs):
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Delete of the OOO.
        """
        return super().delete(request, *args, **kwargs)
