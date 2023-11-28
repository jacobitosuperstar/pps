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
        # creating an admin user
        admin_user = Employee.objects.create_superuser(
            identification="1111111111",
            names="test_super_employee",
            last_names="test_super_employee",
            password="AzQWsX09",
        )
        admin_user.role = RoleChoices.HR
        admin_user.save()
