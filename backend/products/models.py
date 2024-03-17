"""
Product related models
"""
from typing import (
    Any,
    Optional,
    Dict,
    List,
)
from django.utils.translation import gettext as _
from django.db import models
from django.db.models import Q

from base.models import BaseModel


class Product(BaseModel):
    ...
