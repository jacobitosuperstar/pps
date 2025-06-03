from django.forms import Form
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.http import HttpRequest
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
# from django.core.exceptions import (
#     ValidationError,
#     ObjectDoesNotExist,
#     MultipleObjectsReturned,
# )

from base.generic_views import (
    BaseListView,
    BaseFileteredListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)
from base.response import ORJsonResponse as JsonResponse
from base.http_status_codes import HTTP_STATUS as status
from base.logger import base_logger
from employees.decorators import role_validation
from employees.models import RoleChoices
from employees.mixins import (
    AuthenticatedUserMixin,
    RoleValidatorMixin,
)
from .models import (
    SaleOrder,
    SaleOrderItem,
    ProductionOrder,
    ProductionOrderItem,
    QualityEvaluation,
    NonConformingProduct,
)
# from .forms import (
# )


class SaleOrderView(
    RoleValidatorMixin,
    BaseListView,
    BaseCreateView,
):
    model = SaleOrder
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        return super().post(request, *args, **kwargs)


class SaleOrderDUDView(
    RoleValidatorMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    model = SaleOrder
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []


class ProductionOrderView(
    RoleValidatorMixin,
    BaseListView,
    BaseCreateView,
):
    model = ProductionOrder
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []


class ProductionOrderDUDView(
    RoleValidatorMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    model = ProductionOrder
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []


class QualityEvaluationView(
    RoleValidatorMixin,
    BaseListView,
    BaseCreateView,
):
    model = QualityEvaluation
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []


class QualityEvaluationDUDView(
    RoleValidatorMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    model = QualityEvaluation
    form = None
    prefetch_fields = []
    select_fields = []
    serializer_depth: int = 0
    allowed_roles = []


@require_GET
@role_validation(allowed_roles=[RoleChoices.QUALITY])
def non_conforming_products(request: HttpRequest, id: int) -> JsonResponse:
    """Returns a JSON with the list of possible non conforming products that
    belong to a SaleOrder.
    """
    try:
        quality_evaluation: QualityEvaluation = QualityEvaluation.objects.get(id=id)
        msg = {
            "non_conforming_products": quality_evaluation.non_conforming_product_types(),
        }
        return JsonResponse(msg, status=status.ok)
    except QualityEvaluation.DoesNotExist:
        error_data = {"response": _(f"{QualityEvaluation._meta.verbose_name} not found.")}
        return JsonResponse(error_data, status=status.not_found)
    except QualityEvaluation.MultipleObjectsReturned:
        error_data = {
            "response": _(
                f"Multiple entries of type {QualityEvaluation._meta.verbose_name} with id: {id} found."
            )
        }
        return JsonResponse(error_data, status=status.internal_server_error)
    except Exception as e:
        error_data = {"response": _("Internal server error.")}
        base_logger.critical(e)
        return JsonResponse(error_data, status=status.internal_server_error)
