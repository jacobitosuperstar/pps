from typing import (
    List,
    Optional,
)
from typing_extensions import NamedTuple
import json
from rest_framework import serializers
from django import forms
from django.utils.translation import gettext as _

from clients.models import Client
from products.models import Product

from .models import (
    SaleOrder,
    SaleOrderItem,
    ProductionOrder,
    ProductionOrderItem,
    QualityEvaluation,
    NonConformingProduct,
)



class SaleOrderItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    product_ammount = serializers.IntegerField(required=True)

    def validate_product(self, value) -> Product:
        """Checks that the products exists
        """
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("The related product doesn't exists")
        ...


class SaleOrderCreationForm(serializers.Serializer):
    """Form to validate the information regarding the creation of the Product.
    """
    # SaleOrder
    client = serializers.IntegerField(
        required=True,
    )
    notes = serializers.CharField(
        required=False,
    )

    # SaleOrderItem
    items = serializers.JSONField(
        required=True,
    )

    def clean_client(self) -> Client:
        """Checks for the uniqueness of the client id.
        """
        client: int = self.cleaned_data["client"]
        if not Client.objects.filter(id=client).exists():
            raise forms.ValidationError(_("There is not a client with that ID"))
        client_object: Client = Client.objects.get(id=client)
        return client_object

    def clean_items(self) -> List[OrderItem]:
        items_data: dict = json.loads(self.cleaned_data["items"])
        for key, value in items_data:
            if Product.objects.filter(id=value)
        ...


    class Meta:
        fields: list[str] = [
            "client",
            "notes",
            "items",
        ]
