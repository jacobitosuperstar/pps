from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import datetime

from .models import (
    MachineTypes,
    MachineType,
    Machine,
)


class MachineTypeCreationForm(forms.ModelForm):
    """Form to validate that the information send for the user creation is
    valid.
    """
    identification = forms.CharField(
        max_length=50,
        required=True,
    )
    names = forms.CharField(
        max_length=100,
        required=True,
    )
    last_names = forms.CharField(
        max_length=100,
        required=True,
    )
    birthday = forms.DateField(
        required=False,
    )
    role = forms.ChoiceField(
        choices=RoleChoices.choices,
        initial=RoleChoices.PRODUCTION,
        required=True,
    )

    class Meta:
        model = Employee
        fields = [
            "identification",
            "names",
            "last_names",
            "birthday",
            "role",
        ]


class MachineTypeForm(forms.Form):
    """Form to validate that the information send for the user filtering is
    valid.
    """
    machine_type = forms.ChoiceField(
        choices=MachineTypes.choices,
        required=False,
    )
    users_identification = forms.CharField(
        required=False,
    )


class MachineCreationForm(forms.ModelForm):
    """Form to validate the information send for the user to create of filtrate
    a Machine.
    """
    machine_number = forms.CharField(
        max_length=100,
        required=True,
    )
    machine_title = forms.CharField(
        max_length=100,
        required=True,
    )
    machine_type_id = forms.IntegerField(
        required=True,
    )

    class Meta:
        model = Machine
        fields = [
            "machine_number",
            "machine_title",
            "machine_type_id",
        ]

    def clean_machine_type(self):
        machine_type_id = self.cleaned_data["machine_type_id"]
        try:
            machine_type = MachineType.objects.get(
                id=machine_type_id,
            )
            return machine_type
        except Machine.DoesNotExist:
            raise forms.ValidationError(_("Machine not found."))


class MachineForm(forms.Form):
    """Form to validate the information send for the user to create of filtrate
    a Machine.
    """
    machine_number = forms.CharField(
        max_length=100,
        required=False,
    )
    machine_title = forms.CharField(
        max_length=100,
        required=False,
    )
    machine_type_id = forms.IntegerField(
        required=False,
    )

    def clean_machine_type(self):
        machine_type_id = self.cleaned_data.get("machine_type_id")
        if machine_type_id:
            try:
                machine_type = MachineType.objects.get(
                    id=machine_type_id,
                )
                return machine_type
            except Machine.DoesNotExist:
                raise forms.ValidationError(_("Machine not found."))
