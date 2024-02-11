from typing import Dict, Optional, Any, Iterable
from django import forms
from django.utils.translation import gettext as _

from employees.models import Employee
from .models import (
    ExistingMachineTypes,
    MachineType,
    Machine,
)


class MachineTypeCreationForm(forms.Form):
    """Form to validate the information regarding the creation of the machine
    type.
    """
    machine_type = forms.ChoiceField(
        choices=ExistingMachineTypes.choices,
        required=True,
    )
    trained_employees = forms.CharField(
        required=False,
    )

    class Meta:
        model = MachineType
        fields = [
            "machine_type",
            "trained_employees",
        ]

    def clean_trained_employees(self) -> Optional[Iterable[Employee]]:
        """Returns the list of user ids
        """
        raw_employees_ids_list = self.cleaned_data.get("trained_employees")

        if raw_employees_ids_list:

            employees_ids_list = raw_employees_ids_list.split(",")
            employees_ids_list = [
                int(employee_id) for employee_id in employees_ids_list
                if employee_id.isdigit()
            ]

            employees_list = Employee.objects.filter(id__in=employees_ids_list)
            return employees_list


class MachineTypeForm(forms.Form):
    """Form to validate that the information send for the user filtering is
    valid.
    """
    id = forms.IntegerField(
        required=True,
    )
    machine_type = forms.ChoiceField(
        choices=ExistingMachineTypes.choices,
        required=True,
    )
    trained_employees_to_add = forms.CharField(
        required=False,
    )
    trained_employees_to_delete = forms.CharField(
        required=False,
    )

    def clean_trained_employees_to_add(self) -> Optional[Iterable[Employee]]:
        """Returns the list of user ids
        """
        raw_employees_ids_list = self.cleaned_data.get("trained_employees_to_add")

        if raw_employees_ids_list:

            employees_ids_list = raw_employees_ids_list.split(",")
            employees_ids_list = [
                int(employee_id) for employee_id in employees_ids_list
                if employee_id.isdigit()
            ]

            employees_list = Employee.objects.filter(id__in=employees_ids_list)
            return employees_list

    def clean_trained_employees_to_delete(self) -> Optional[Iterable[Employee]]:
        """Returns the list of user ids
        """
        raw_employees_ids_list = self.cleaned_data.get("trained_employees_to_delete")

        if raw_employees_ids_list:

            employees_ids_list = raw_employees_ids_list.split(",")
            employees_ids_list = [
                int(employee_id) for employee_id in employees_ids_list
                if employee_id.isdigit()
            ]

            employees_list = Employee.objects.filter(id__in=employees_ids_list)
            return employees_list


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
    machine_type = forms.IntegerField(
        required=True,
    )

    class Meta:
        model = Machine
        fields = [
            "machine_number",
            "machine_title",
            "machine_type",
        ]

    def clean_machine_type(self) -> Optional[MachineType]:
        machine_type_id = self.cleaned_data["machine_type"]
        try:
            machine_type = MachineType.objects.get(
                id=machine_type_id,
            )
            return machine_type
        except MachineType.DoesNotExist:
            raise forms.ValidationError(_("Machine type not found."))

    def clean(self) -> Optional[Dict[str, Any]]:
        cleaned_data = super().clean()
        machine_title = cleaned_data["machine_title"]
        machine_number = cleaned_data["machine_number"]

        if Machine.objects.filter(
            machine_title=machine_title,
            machine_number=machine_number,
        ).exists():
            raise forms.ValidationError(
                _("A machine with this number and title already exists.")
            )


class MachineForm(forms.Form):
    """Form to validate the information send for the user to create of filtrate
    a Machine.
    """
    machine_id = forms.IntegerField(
        required=True,
    )
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

    def clean_machine_type(self) -> Optional[MachineType]:
        machine_type_id = self.cleaned_data.get("machine_type")
        if machine_type_id:
            try:
                machine_type = MachineType.objects.get(
                    id=machine_type_id,
                )
                return machine_type
            except MachineType.DoesNotExist:
                raise forms.ValidationError(_("Machine type not found."))
