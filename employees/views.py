import secrets
from django.shortcuts import render
from django.http import HttpRequest
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.views.decorators.csrf import (
    csrf_exempt,
    # ensure_csrf_cookie,
)
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse
# serverilio
from .decorators.validation import (
    role_validation,
)

# Create your views here.
