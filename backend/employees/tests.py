import secrets
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from base.http_status_codes import HTTP_STATUS as status
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
        response = self.client.post(
            reverse(viewname="login"),
            data=msg,
        )
        return

    def test_pin(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="pin"))
        self.assertEqual(response.status_code, status.ok)
        print("\n")

    def test_logged_pin(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="logged_pin"))
        self.assertEqual(response.status_code, status.ok)
        print("\n")

    def test_employee_roles(self):
        """Test to get all the employee roles
        """
        response = self.client.get(reverse(viewname="roles"))
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.ok)
        print("\n")

    def test_employee_ooo_types(self):
        """Test to get all the employee roles
        """
        response = self.client.get(reverse(viewname="ooo_types"))
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.ok)
        print("\n")

    def test_get_list_of_empoloyees(self):
        """Test to get all the employess
        """
        response = self.client.get(reverse(viewname="list_employees"))
        if response.status_code == status.ok:
            for chunk in response.streaming_content:
                print(json.loads(chunk))
        else:
            print(json.loads(response.content))
        print("\n")

    def test_get_empoloyee(self):
        """Test to get all the employess
        """
        response = self.client.get(
            reverse(
                viewname="get_employee",
                args=["1111111111"]
                # args=["1111111112"]
            )
        )
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.ok)
        print("\n")

    def test_create_prod_employee(self):
        """Test to create a production user
        """
        self.admin_user.role = RoleChoices.HR
        self.admin_user.save()

        msg = {
            "identification": "1111111111",
            "password": "AzQWsX09",
        }
        response = self.client.post(
            reverse(viewname="login"),
            data=msg,
        )

        msg = {
            "identification": "222222222222",
            "names": "test_employee",
            "last_names": "test_employee",
            "role": RoleChoices.PRODUCTION,
        }
        response = self.client.post(
            reverse(viewname="create_employee"),
            data=msg,
        )
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.created)
        print("\n")

    def test_create_non_prod_employee(self):
        """Test to create a non production user
        """
        self.admin_user.role = RoleChoices.HR
        self.admin_user.save()

        msg = {
            "identification": "1111111111",
            "password": "AzQWsX09",
        }
        response = self.client.post(
            reverse(viewname="login"),
            data=msg,
        )

        msg = {
            "identification": "333333333333",
            "names": "test_employee",
            "last_names": "test_employee",
            "password": "AzQWsX09",
            "role": RoleChoices.PRODUCTION_MANAGER
        }
        response = self.client.post(
            reverse(viewname="create_employee"),
            data=msg,
        )
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.created)
        print("\n")
