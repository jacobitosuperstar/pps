from typing import Optional
from django import forms
from django.utils.translation import gettext as _

from .models import (
    Client,
)

class ClientCreationForm(forms.Form):
    """Form to validate the information regarding the creation of the Product.
    """
    client_id = forms.CharField(
        required=True,
    )
    client_name = forms.CharField(
        required=True,
    )
    client_email = forms.EmailField(
        required=True,
    )
    client_phone_code = forms.CharField(
        required=False,
    )
    client_phone_number = forms.CharField(
        required=True,
    )

    def clean_client_id(self) -> str:
        """Checks for the uniqueness of the client id.
        """
        client_id = self.cleaned_data["client_id"]
        if Client.objects.filter(client_id=client_id).exists():
            raise forms.ValidationError(_("There is already a client with that ID."))
        return client_id

    class Meta:
        model = Client
        fields: list[str] = [
            "client_id",
            "client_name",
            "client_email",
            "client_phone_code",
            "client_phone_number",
        ]


class ClientUpdateForm(forms.Form):
    """Form to validate the information regarding the creation of the Product.
    """
    client_id = forms.CharField(
        required=False,
    )
    client_name = forms.CharField(
        required=False,
    )
    client_email = forms.EmailField(
        required=False,
    )
    client_phone_code = forms.CharField(
        required=False,
    )
    client_phone_number = forms.CharField(
        required=False,
    )

    def clean_client_id(self) -> Optional[str]:
        """Checks for the uniqueness of the client id.
        """
        client_id = self.cleaned_data.get("client_id")
        if Client.objects.filter(client_id=client_id).exists() and client_id:
            raise forms.ValidationError(_("There is already a client with that ID."))
        return client_id


class ClientForm(forms.Form):
    """Form to validate the information regarding the creation of the Product.
    """
    client_id = forms.CharField(
        required=False,
    )
    client_name = forms.CharField(
        required=False,
    )
    client_email = forms.EmailField(
        required=False,
    )
    client_phone_code = forms.CharField(
        required=False,
    )
    client_phone_number = forms.CharField(
        required=False,
    )
