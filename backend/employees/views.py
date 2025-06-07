import secrets
from django.http import (
    HttpRequest,
)
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.forms import ValidationError

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema

from base.response import ORJsonResponse as JsonResponse
from base.http_status_codes import HTTP_STATUS
from base.logger import base_logger
from base.generic_views import (
    BaseFileteredListView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

from jwt_authentication.jwt_authentication import JWTAuthentication, create_token

from .decorators import IsEmployeeRole, role_validation
from .mixins import (
    RoleValidatorMixin,
)

from .models import (
    Employee,
    RoleChoices,
    OOO,
    OOOTypes_list,
    Role_list
)
from .forms import (
    EmployeeForm,
    OOOForm,
)

from .serializers import (
    CommonFilterSerializer,
    CreateEmployeeSerializer,
    EmployeeAuthenticationSerializer,
    EmployeeLoginResponseSerializer,
    EmployeeOptionSerializer,
    EmployeeSerializer,
    ErrorResponseSerializer,
    OOOTypesResponseSerializer,
    RoleChoicesResponseSerializer,
    UpdateEmployeeSerializer,
    OOOSerializer,
    CreateOOOSerializer,
    UpdateOOOSerializer
)

############################
###### Rest Framework ######
############################
@extend_schema(tags=["Authentication"])
class EmployeeLoginView(APIView):
    serializer_class = EmployeeAuthenticationSerializer

    @extend_schema(
        description="Login endpoint for employees.",
        request=EmployeeAuthenticationSerializer,
        responses={
            status.HTTP_200_OK: EmployeeLoginResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer,
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                "response": _("Error in the information given"),
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        identification = serializer.validated_data['identification']
        password = serializer.validated_data['password']
        employee = authenticate(
            request,
            identification=identification,
            password=password
        )
        if not employee:
            msg = {
                "response": _("Invalid credentials, check the ID or the Password"),
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        token = create_token(
            employee_id=employee.id,
            employee_role=employee.role,
        )

        serialized_employee = EmployeeSerializer(employee, context={"request": request})

        msg = {
            "response": _("Logged in successfully"),
            "employee": serialized_employee.data,
            "token": token,
        }
        return Response(msg, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Employees"])
class EmployeeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeRole(['admin', 'hr'])]
    serializer_class = EmployeeSerializer
    renderer_classes = [JSONRenderer]
    
    @extend_schema(
        parameters=[CommonFilterSerializer],
        responses=EmployeeSerializer,
        description="List all employees.",
    )
    def list(self, request):
        filter_serializer = CommonFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data
        
        queryset = Employee.objects.filter(is_active=True)

        # Filtro de búsqueda por nombre, apellido o identificación
        search = filters.get('search')

        if search:
            queryset = queryset.filter(
                Q(identification__icontains=search) |
                Q(names__icontains=search) |
                Q(last_names__icontains=search)
            )

        # Paginación
        paginator = PageNumberPagination()
        paginator.page_size = filters.get('page_size', 10)
        paginated_qs = paginator.paginate_queryset(queryset, request)

        serializer = EmployeeSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @extend_schema(
        parameters=[CommonFilterSerializer],
        responses=EmployeeOptionSerializer,
        description="Options endpoint for autocomplete dropdowns with infinite scroll.",
    )
    @action(detail=False, methods=['get'], url_path='options')
    def options(self, request):
        search = request.query_params.get("search", "")
        queryset = Employee.objects.filter(is_active=True)

        if search:
            queryset = queryset.filter(
                Q(identification__icontains=search) |
                Q(names__icontains=search) |
                Q(last_names__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        paginated_qs = paginator.paginate_queryset(queryset, request)

        serializer = EmployeeOptionSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    

    @extend_schema(
        responses=EmployeeSerializer,
        description="Retrieve a single employee by ID.",
    )
    def retrieve(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


    @action(detail=False, methods=["get"], url_path="roles")
    @extend_schema(
        description="List of work roles for the different kind of employees.",
        responses={
            status.HTTP_200_OK: RoleChoicesResponseSerializer(many=True),
        }
    )
    def get_roles(self, request):
        return Response(Role_list, status=status.HTTP_200_OK)

    @extend_schema(
        request=CreateEmployeeSerializer,
        responses=EmployeeSerializer,
        description="Create a new employee.",
    )
    def create(self, request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    @extend_schema(
        request=UpdateEmployeeSerializer,
        responses=EmployeeSerializer,
        description="Update an employee by ID.",
    )
    def update(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateEmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="deactivate")
    @extend_schema(
        responses=EmployeeSerializer,
        description="Deactivate an employee (mark as is_deleted=True)."
    )
    def deactivate(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not employee.is_active:
            return Response({"detail": "Employee is already deactivated."}, status=status.HTTP_400_BAD_REQUEST)

        employee.is_active = False
        employee.save()

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["OOO"])
class OOOViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsEmployeeRole(['admin', 'hr'])]
    serializer_class = OOOSerializer
    renderer_classes = [JSONRenderer]

    @extend_schema(
        parameters=[CommonFilterSerializer],
        responses=OOOSerializer,
        description="List all OOO (Out Of Office) records with optional filters.",
    )
    def list(self, request):
        filter_serializer = CommonFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        queryset = OOO.objects.select_related("employee").all()

        # Filtro de búsqueda por nombre del empleado o tipo de OOO
        search = filters.get('search')
        if search:
            queryset = queryset.filter(
                Q(employee__names__icontains=search) |
                Q(employee__last_names__icontains=search) |
                Q(employee__identification__icontains=search)
            )

        # Paginación
        paginator = PageNumberPagination()
        paginator.page_size = filters.get('page_size', 10)
        paginated_qs = paginator.paginate_queryset(queryset, request)

        serializer = OOOSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        responses=OOOSerializer,
        description="Retrieve a single OOO record by ID.",
    )
    def retrieve(self, request, pk=None):
        try:
            ooo = OOO.objects.get(pk=pk)
        except OOO.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OOOSerializer(ooo)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="types")
    @extend_schema(
        description="List of out-of-office types for employees.",
        responses={status.HTTP_200_OK: OOOTypesResponseSerializer},
    )
    def get_types(self, request):
        return Response(OOOTypes_list, status=status.HTTP_200_OK)

    @extend_schema(
        request=CreateOOOSerializer,
        responses=OOOSerializer,
        description="Create a new OOO (Out Of Office) record.",
    )
    def create(self, request):
        serializer = CreateOOOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=UpdateOOOSerializer,
        responses=OOOSerializer,
        description="Update an existing OOO record by ID.",
    )
    def update(self, request, pk=None):
        try:
            ooo = OOO.objects.get(pk=pk)
        except OOO.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateOOOSerializer(ooo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################
###### Django Generic ######
############################

class EmployessFilteredView(
    RoleValidatorMixin,
    BaseFileteredListView
):
    allowed_roles = [
        RoleChoices.HR,
        RoleChoices.MANAGEMENT,
        RoleChoices.PRODUCTION_MANAGER,
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
            return JsonResponse(msg, status=HTTP_STATUS.accepted)
        except ValidationError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=HTTP_STATUS.bad_request)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=HTTP_STATUS.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=HTTP_STATUS.internal_server_error)

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
            return JsonResponse(msg, status=HTTP_STATUS.accepted)
        except self.model.DoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=HTTP_STATUS.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=HTTP_STATUS.internal_server_error)


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
