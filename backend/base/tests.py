# Create your tests here.
import json
from django.test import TestCase, Client
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import Employee


class AuthTokenWorkflowTest(TestCase):
    """
    """
    def setUp(self) -> None:
        # setting up the django client
        self.client = Client()
        # creating an admin user
        self.admin_user: Employee = Employee.objects.create_superuser(
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

        response = self.client.post(
            reverse(viewname="login"),
            data=msg,
        )
        response = json.loads(response.content)
        token = response.get("token")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Token {token}"
        return

    def test_pin(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="pin"))
        # print(response.content)
        self.assertEqual(response.status_code, status.ok)

    def test_logged_pin(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="logged_pin"))
        # print(response.content)
        self.assertEqual(response.status_code, status.ok)
