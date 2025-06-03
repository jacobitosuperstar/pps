from typing_extensions import TypedDict
# from pydantic import BaseModel


class SaleOrderItem(TypedDict):
    product: int
    product_amount: int


class SaleOrder(TypedDict):
    client: int
    notes: str
    items: list[SaleOrderItem]


class ProductionOrderItem(TypedDict):
    product: int
    product_amount: int


class ProductionOrder(TypedDict):
    client: int
    notes: str
    items: list[SaleOrderItem]
