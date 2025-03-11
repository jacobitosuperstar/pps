"""Production related models.
"""
from typing import (
    List,
    Dict,
    Any,
)
from django.db import models
from django.db.models.query import QuerySet

from base.models import BaseModel
from products.models import Product
from clients.models import Client


class SaleOrder(BaseModel):
    """Production order.

    Parameters
    ----------
    client: Client
        Client to which the product will be delivered.
    notes: str
        Notes from the commercial that are needed to be taken into account for
        this production order.
    delivery_date: DateTime
        Date on which the product must be delivered to the client.
    """
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
    )
    notes = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "sale_order"
        verbose_name = "sale_order"
        verbose_name_plural = "sale_orders"


class SaleOrderItem(BaseModel):
    """Production order Items.

    Parameters
    ----------
    product: Product
        Product that is going to be produced in this particular order.
    product_ammount: int
        Ammount of Product needed to be made for this order to be fullfilled.
    """
    sale_order = models.ForeignKey(
        to=SaleOrder,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )
    product_ammount = models.IntegerField(default=0)

    class Meta:
        db_table = "sale_order_item"
        verbose_name = "sale_order_item"
        verbose_name_plural = "sale_order_items"


class ProductionOrder(BaseModel):
    """Production order.

    Parameters
    ----------
    client: Client
        Client to which the product will be delivered.
    """
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
    )
    notes = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "production_order"
        verbose_name = "production_order"
        verbose_name_plural = "production_orders"


class ProductionOrderItem(BaseModel):
    """Production order Items.

    Parameters
    ----------
    product: Product
        Product that is going to be produced in this particular order.
    product_ammount: int
        Ammount of Product needed to be made for this order to be fullfilled.
    notes: str
        Notes from the commercial that are needed to be taken into account for
        this production order.
    delivery_date: DateTime
        Date on which the product must be delivered to the client.
    """
    production_order = models.ForeignKey(
        to=ProductionOrder,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )
    product_ammount = models.IntegerField(
        default=0,
    )

    class Meta:
        db_table = "production_order_item"
        verbose_name = "production_order_item"
        verbose_name_plural = "production_order_items"


class QualityEvaluation(BaseModel):
    """Evaluation of the execution of the production order.

    After the Production Order is completed and sended to the buyer, there are
    observations that are needed to be done in case we have non conforming
    product, send an erronious ammount or some other eventuality happens that
    may compromise the initial time calculated for the production order.

    If no observations are detected, the delivery time should be the same that
    the one present in the Production Order so that the indicator is not
    affected.

    Parameters
    ----------
    sale_order: SaleOrder
        Sale Order that is going to be evaluated.
    notes: str
        Observations or notes made from the Quality personel, regarding the
        production.
    delivery_date: DateTime
        Date on which the Production Order was succesfully delivered.
    """
    sale_order = models.ForeignKey(
        to=SaleOrder,
        on_delete=models.CASCADE,
    )
    notes = models.TextField(
        null=True,
        blank=True,
    )
    delivery_date = models.DateField()

    class Meta:
        db_table = "quality_evaluation"
        verbose_name = "quality_evaluation"
        verbose_name_plural = "quality_evaluations"

    def non_conforming_product_types(self) -> List[Dict[str, Any]]:
        """Returns all the non conforming items that can be in the SaleOrder.
        """
        saleOrderItems: QuerySet[SaleOrderItem] = SaleOrderItem.objects.filter(sale_order=self.sale_order)
        serialized_saleOrderItems: List[Dict[str, Any]] = [value.serializer() for value in saleOrderItems]
        return serialized_saleOrderItems


class NonConformingProduct(BaseModel):
    """Non conforming production order items.

    Parameters
    ----------
    quality_evaluation: QualityEvaluation
        Parent QualityEvaluation.
    non_conforming_product: SaleOrderItem
        Non conforming product from the SaleOrder.
    non_conforming_product_ammount: int
        Ammount of product deemed not up to standard to the client.
    """
    quality_evaluation = models.ForeignKey(
        to=QualityEvaluation,
        on_delete=models.CASCADE,
    )
    non_conforming_product = models.ForeignKey(
        to=SaleOrderItem,
        on_delete=models.CASCADE,
    )
    non_conforming_product_ammount = models.IntegerField(
        default=0,
    )

    class Meta:
        db_table = "non_conforming_product"
        verbose_name = "non_conforming_product"
        verbose_name_plural = "non_conforming_products"
