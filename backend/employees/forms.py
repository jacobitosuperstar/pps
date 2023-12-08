from django import forms
from django.core.validators import EMPTY_VALUES
from .models import (
    Employee,
    RoleChoices,
    OOO,
    OOOTypes,
)


class EmployeeAuthenticationForm(forms.Form):
    """Form to validate the log in information."""
    identification = forms.CharField(
        max_length=50,
        required=True,
    )
    password = forms.CharField(
        required=True,
    )


class EmployeeCreationForm(forms.ModelForm):
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


class EmployeeForm(forms.Form):
    """Form to validate that the information send for the user filtering is
    valid.
    """
    identification = forms.CharField(
        max_length=50,
        required=False,
    )
    names = forms.CharField(
        max_length=100,
        required=False,
    )
    last_names = forms.CharField(
        max_length=100,
        required=False,
    )
    birthday = forms.DateField(
        required=False,
    )
    role = forms.ChoiceField(
        choices=RoleChoices.choices,
        required=False,
    )
    is_active = forms.BooleanField(required=False,)


class OOOCreationForm(forms.ModelForm):
    """Form to validate the information send for the user and create an OOO.
    """
    employee_identification = forms.CharField(
        max_length=50,
    )
    ooo_type = forms.ChoiceField(
        choices=OOOTypes.choices,
    )
    start_date = forms.DateField()
    end_date = forms.DateField()
    description = forms.CharField()

    class Meta:
        model = OOO
        fields = [
            "employee_identification",
            "ooo_type",
            "start_date",
            "end_date",
            "description",
        ]

    def clean_employee(self):
        try:
            employee_identification = self.cleaned_data.get("employee_identification")
            employee = Employee.objects.get(
                identification=employee_identification,
            )
            return employee
        except Employee.DoesNotExist:
            raise forms.ValidationError(_("Employee not found."))
