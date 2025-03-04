from django import forms
from django.utils.translation import gettext as _

from .models import (
    Product,
)


class ProductCreationForm(forms.Form):
    """Form to validate the information regarding the creation of the Product.
    """
    name = forms.CharField(
        required=True,
    )
    materials = forms.JSONField(
        required=False,
    )

    def clean_name(self):
        """Checks for the uniqueness of the product name.
        """
        name = self.cleaned_data["name"]
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError(_("There is already a product with that name."))
        return name

    class Meta:
        model = Product
        fields = [
            "name",
            "materials",
        ]

class ProductUpdateForm(forms.Form):
    """Form to validate the information regarding Product.
    """
    name = forms.CharField(
        required=False,
    )
    materials = forms.JSONField(
        required=False,
    )

    def clean_name(self):
        """Checks for the uniqueness of the product name.
        """
        name = self.cleaned_data["name"]
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError(_("There is already a product with that name."))
        return name


class ProductForm(forms.Form):
    """Form to validate the information regarding Product.
    """
    name = forms.CharField(
        required=False,
    )
