from django.core.management.base import BaseCommand
from employees.models import (
    RoleChoices,
    Employee,
)


class Command(BaseCommand):
    """Command to create a dummy HR person to do the tests.

    Example
    -------
    >>> python manage.py test_environ
    """
    help = "Query the metadata from the Buildings"

    def handle(
        self,
        *args,
        **options,
    ):
        """Handle of the test_environ command."""
        # creating an admin HR user
        admin_user = Employee.objects.create_superuser(
            identification="1111111111",
            names="test_super_employee_HR",
            last_names="test_super_employee_HR",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.HR
        admin_user.save()

        # creating an admin PRODUCTION_MANAGER user
        admin_user = Employee.objects.create_superuser(
            identification="2222222222",
            names="test_super_employee_PM",
            last_names="test_super_employee_PM",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.PRODUCTION_MANAGER
        admin_user.save()

        # creating an admin MANAGEMENT user
        admin_user = Employee.objects.create_superuser(
            identification="3333333333",
            names="test_super_employee_M",
            last_names="test_super_employee_M",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.MANAGEMENT
        admin_user.save()

        # quality
        admin_user = Employee.objects.create_superuser(
            identification="4444444444",
            names="test_super_employee_Q",
            last_names="test_super_employee_Q",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.QUALITY
        admin_user.save()

        # accounting
        admin_user = Employee.objects.create_superuser(
            identification="5555555555",
            names="test_super_employee_A",
            last_names="test_super_employee_A",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.ACCOUNTING
        admin_user.save()
