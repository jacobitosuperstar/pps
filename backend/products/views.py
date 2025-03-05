from django.forms import Form
from django.utils.decorators import method_decorator
from django.http import HttpRequest

from base.generic_views import (
    BaseListView,
    BaseFileteredListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)
from base.response import ORJsonResponse as JsonResponse
from employees.decorators import role_validation
from employees.models import RoleChoices
from employees.mixins import (
    AuthenticatedUserMixin,
)
from .models import (
    Product,
)
from .forms import (
    ProductCreationForm,
    ProductUpdateForm,
    ProductForm,
)


class ProductView(
    AuthenticatedUserMixin,
    BaseListView,
    BaseCreateView,
):
    """View Class to chandle the creation of the Product model objects.
    """
    model: type[Product] = Product
    form: type[Form] = ProductCreationForm
    serializer_depth: int = 0

    @method_decorator(
        decorator=role_validation(
            allowed_roles=[
                RoleChoices.PRODUCTION_MANAGER,
                RoleChoices.MANAGEMENT,
            ]
        )
    )
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Creation of the Product.
        """
        return super().post(request, *args, **kwargs)


class ProductFilteredView(
    AuthenticatedUserMixin,
    BaseFileteredListView,
):
    """View Class based view to handle the filtering and listing the objects.
    """
    model: type[Product] = Product
    form: type[Form] = ProductForm
    serializer_depth: int = 0


class ProductDUDView(
    AuthenticatedUserMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    """View Class to handle the deatiled view, the update and the delete of the
    Product model object.
    """
    model: type[Product] = Product
    form: type[Form] = ProductUpdateForm
    url_kwarg: str = "id"

    @method_decorator(
        decorator=role_validation(
            allowed_roles=[
                RoleChoices.PRODUCTION_MANAGER,
                RoleChoices.MANAGEMENT,
            ]
        )
    )
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Update of the Product.
        """
        return super().post(request, *args, **kwargs)

    @method_decorator(
        decorator=role_validation(
            allowed_roles=[
                RoleChoices.PRODUCTION_MANAGER,
                RoleChoices.MANAGEMENT,
            ]
        )
    )
    def delete(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """This method is re defined because there are different permissions to
        different methods within the endpoint. The main idea would be to
        assign the roles that can use this http method.

        Deletion of the Product.
        """
        return super().delete(request, *args, **kwargs)
