"""Products related models

Product:
    Items created from the company that are being sold to different clients.
"""
from django.db import models

from base.models import BaseModel


class Product(BaseModel):
    """Items created from the company that are being sold to different clients.

    Parameters
    ----------
    name: str
        Name of the product.
    materials: dict
        Dictonary of materials and ammounts needed for the creation of the
        product.
    """
    name = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        unique=True,
    )
    materials = models.JSONField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
