import json
from django.test import TestCase, Client
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import RoleChoices, Employee
from clients.models import Client as CompanyClient


class ClientsWorkflowTest(TestCase):
    """
    """
    def setUp(self) -> None:
        # setting up the django client
        self.client = Client()
        # creating a production manager to test the application module
        self.admin_user: Employee = Employee.objects.create_superuser(
            identification="1111111111",
            names="test_super_employee",
            last_names="test_super_employee",
            password="AzQWsX09",
        )
        self.admin_user.role = RoleChoices.PRODUCTION_MANAGER
        # self.admin_user.role = RoleChoices.HR
        self.admin_user.save()

        self.company_client = CompanyClient.objects.create(
            client_id="1111111111",
            client_name="TestClient1",
            client_email="client@test.com",
            client_phone_number="1111111111",
        )

        CompanyClient.objects.create(
            client_id="2222222222",
            client_name="TestClient2",
            client_email="client@test.com",
            client_phone_number="2222222222",
        )

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

    def test_get_list_of_clients(self):
        ...

    def test_list_filtered_clients(self):
        ...

    def test_get_client(self):
        ...

    def test_create_client(self):
        ...

    def test_update_client(self):
        ...

    def test_delete_client(self):
        ...
