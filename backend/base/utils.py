from typing import (
    Optional,
    Generator,
    Any,
    List,
)
from django.db import models
from django.db.models.base import Model  # isort:skip
from django.db.models import QuerySet


def model_list_generator(
    model: Model,
    queryset: QuerySet,
    fields_to_exclude: List[Optional[str]],
) -> Generator[Any, Any, Any]:
    """."""
    # Get the model's list of field names
    fields = [
        field for field in model._meta.get_fields()
        if not field.one_to_many
    ]

    # converting the query list into dicts
    for element in queryset:
        serialized_data = {}
        for field in fields:
            field_name = field.name

            if isinstance(field, models.ForeignKey):
                field_value =
        yield {field: getattr(element, field) for field in fields}
