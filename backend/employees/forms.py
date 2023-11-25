from django import forms
from django.core.validators import EMPTY_VALUES
from .models import Employee, RoleChoices


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
    """Form to validate that the information send for the user filterin is
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
        choices=RoleChoices,
        required=False,
    )
    is_active = forms.BooleanField(required=False,)
