from typing import (
    List,
    Dict,
    Any,
    Optional,
)
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base fields that all database models should have.

    Non Database Attributes
    -----------------------
    PRIVATE_FIELDS: List[Optional[str]]
        Fields that we don't want to show when we serialize the object.

    Fields
    ------
    created_at: DateTime
        Creation time of the row.
    updated_at: DateTime
        Updated time of the row.
    is_deleted: Bool
        Soft deletion of the element of the row.
    """
    PRIVATE_FIELDS: List[Optional[str]] = []

    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    is_deleted = models.BooleanField(default=False,)

    class Meta:
        abstract = True

    def serializer(self) -> Dict[str, Any]:
        """Returns a dict object with the corresponding fields and values that
        you want to serialize.
        """
        # get the model of the object
        model = self._meta.model
        # getting the fields of the model. We skip over the PRIVATE_FIELDS and
        # the fields that are of type one_to_many.
        fields = [
            field for field in model._meta.get_fields()
            if not field.one_to_many
            and field.name not in self.PRIVATE_FIELDS
        ]

        # This is where we are going to store the fields and the values of the
        # object
        serialized_object = {}

        for field in fields:
            field_name = field.name
            field_value = getattr(self, field_name)

            if isinstance(field, models.ForeignKey):
                field_value = field_value.serializer()

            if isinstance(field, (models.DateTimeField, models.DateField)):
                field_value = field_value.isoformat() if field_value else None

            if isinstance(field, models.ManyToManyField):
                field_value = [item.serializer() for item in field_value.all()]

            if isinstance(field, models.ManyToManyRel):
                field_value = [item.serializer() for item in field_value.all()]

            serialized_object[field_name] = field_value

        return serialized_object
