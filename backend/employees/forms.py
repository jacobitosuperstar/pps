from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import datetime

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
        required=True,
    )
    ooo_type = forms.ChoiceField(
        choices=OOOTypes.choices,
        required=True,
    )
    start_date = forms.DateTimeField(
        required=True,
    )
    end_date = forms.DateTimeField(
        required=True,
    )
    description = forms.CharField(
        required=True,
    )

    class Meta:
        model = OOO
        fields = [
            "employee_identification",
            "ooo_type",
            "start_date",
            "end_date",
            "description",
        ]

    def clean_employee_identification(self):
        try:
            employee_identification = self.cleaned_data["employee_identification"]
            employee = Employee.objects.get(
                identification=employee_identification,
            )
            return employee
        except Employee.DoesNotExist:
            raise forms.ValidationError(_("Employee not found."))
        except Employee.MultipleObjectsReturned:
            raise forms.ValidationError(_("Several Employees with the same document found."))

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]
        try:
            start_date = datetime.fromisoformat(start_date)
        except ValueError:
            raise forms.ValidationError(_("Invalid ISO format."))
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        try:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
        except ValueError:
            raise forms.ValidationError(_("Invalid ISO format."))
        if end_date <= start_date:
            raise forms.ValidationError(_("End date must be after start date."))
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
        return end_date


class OOOForm(forms.Form):
    """Form to validate the information send for the user and create an OOO.
    """
    employee_identification = forms.CharField(
        max_length=50,
        required=False,
    )
    ooo_type = forms.ChoiceField(
        choices=OOOTypes.choices,
        required=False,
    )
    start_date = forms.DateTimeField(
        required=False,
    )
    end_date = forms.DateTimeField(
        required=False,
    )

    def clean_employee_identification(self):
        employee_identification = self.cleaned_data.get("employee_identification")
        if employee_identification:
            try:
                employee = Employee.objects.get(
                    identification=employee_identification,
                )
                return employee
            except Employee.DoesNotExist:
                raise forms.ValidationError(_("Employee not found."))
            except Employee.MultipleObjectsReturned:
                raise forms.ValidationError(_("Several Employees with the same document found."))

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date)
            except ValueError:
                raise forms.ValidationError(_("Invalid ISO format."))
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
            return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if start_date and end_date:
            try:
                start_date = datetime.fromisoformat(start_date)
                end_date = datetime.fromisoformat(end_date)
            except ValueError:
                raise forms.ValidationError(_("Invalid ISO format."))
            if end_date <= start_date:
                raise forms.ValidationError(_("End date must be after start date."))
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
            return end_date
