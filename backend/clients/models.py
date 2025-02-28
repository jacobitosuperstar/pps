"""Clients related models.

Client:
    Clients to which the company generates production orders.
"""

from django.utils.translation import gettext as _
from django.db import models

from base.models import BaseModel

class Client(BaseModel):
    """Clients to which the company generates production orders.

    Parameters
    ----------
    client_id: str
        Idenfitication number of the client.
    client_name: str
        Name of the client.
    client_email: str
        Email of the client.
    client_phone_code: int
        Country code phone number.
    client_email: str
        Client phone number.
    """

    client_id = models.CharField(
        # index=True,
        null=False,
        blank=False,
        unique=True,
    )
    client_name = models.CharField(
        null=False,
        blank=False,
    )
    client_email = models.EmailField(
        null=False,
        blank=False,
    )
    client_phone_code = models.CharField(
        max_length=10,
        default="+57",
    )
    client_phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "client"
        indexes = [
            models.Index(fields=["client_id"]),
        ]
        verbose_name = "client"
        verbose_name_plural = "clients"
