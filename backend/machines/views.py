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
    MachineTypes_dict,
    MachineType,
    Machine,
)

from .forms import (
    MachineCreationForm,
    MachineForm,
)

from .decorators import (
    role_validation,
)


@require_GET
@authenticated_user
def machine_types_view(request: HttpRequest) -> JsonResponse:
    """List of the current machine types in the company. Do not confuse this
    view with the other machine type, that is where we store the type of
    machines that exists and also store the employees that are trained to use
    those types of machinery.
    """
    return JsonResponse(MachineTypes_dict)
