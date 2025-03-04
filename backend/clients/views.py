from base.generic_views import (
    BaseCreateView,
    BaseListView,
    BaseFileteredListView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)
from employees.mixins import RoleValidatorMixin
from employees.models import RoleChoices

from .models import (
    Client,
)
from .forms import (
    ClientCreationForm,
    ClientForm,
    ClientUpdateForm,
)


class ClientView(
    RoleValidatorMixin,
    BaseCreateView,
    BaseListView,
):
    allowed_roles = [
        RoleChoices.MANAGEMENT,
        RoleChoices.ACCOUNTING,
    ]
    model: type[Client] = Client
    form: type[ClientCreationForm] = ClientCreationForm
    serializer_depth = 0


class ClientFilteredView(
    RoleValidatorMixin,
    BaseFileteredListView,
):
    allowed_roles = [
        RoleChoices.MANAGEMENT,
        RoleChoices.ACCOUNTING,
    ]
    model: type[Client] = Client
    form: type[ClientForm] = ClientForm


class ClientDUDView(
    RoleValidatorMixin,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    """View Class to handle the deatiled view, the update and the delete of the
    Product model object.
    """
    allowed_roles = [
        RoleChoices.MANAGEMENT,
        RoleChoices.ACCOUNTING,
    ]
    model: type[Client] = Client
    form: type[ClientUpdateForm] = ClientUpdateForm
    url_kwarg: str = "client_id"
