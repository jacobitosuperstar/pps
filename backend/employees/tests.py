import secrets
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from employees.models import RoleChoices, Employee


class AuthTokenWorkflowTest(TestCase):
    """
    """
    def setUp(self) -> None:
        # setting up the django client
        self.client = Client()
        # creating an admin user
        self.admin_user = Employee.objects.create_superuser(
            identification="1111111111",
            names="test_super_employee",
            last_names="test_super_employee",
            password="AzQWsX09",
        )
        self.admin_user.save()
        msg = {
            "identification": "1111111111",
            "password": "AzQWsX09",
        }
        self.client.post(
            reverse(viewname="login"),
            data=msg,
        )
        return

    def test_pin(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="check_server"))
        # status verification
        print(response.content)
        self.assertEqual(response.status_code, 200)
