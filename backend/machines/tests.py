import json
from django.test import TestCase, Client
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import RoleChoices, Employee, OOOTypes
from machines.models import ExistingMachineTypes


class AuthTokenWorkflowTest(TestCase):
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

    def test_existing_machine_types(self):
        """Tets the state of the server.
        """
        response = self.client.get(reverse(viewname="existing_machine_types"))
        self.assertEqual(response.status_code, status.ok)

    def test_create_update_and_list_machine_type(self):
        """Tests Creation, Update, Deletion and listing of the machine types
        created.
        """
        # CREATE MACHINE TYPE
        msg = {
            "machine_type": ExistingMachineTypes.PI,
            "trained_employees": [self.admin_user.id],
        }
        response = self.client.post(
            reverse(viewname="create_machine_type"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)

        # taking the information from the created machine
        response_info = json.loads(response.content)
        created_machine_type_info = response_info["machine_type"]

        # LIST EXISTING MACHINE TYPES
        response = self.client.get(reverse(viewname="list_machine_types"))
        self.assertEqual(response.status_code, status.ok)

        # UPDATES MACHINE TYPES
        msg = {
            "id": created_machine_type_info["id"], # ID from the created machine in the test
            "machine_type": ExistingMachineTypes.PE,
            "trained_employees_to_delete": [self.admin_user.id],
        }

        response = self.client.post(
            reverse(viewname="update_machine_type"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.accepted)

        # DELETE MACHINE TYPE
        response = self.client.delete(
            reverse(
                viewname="delete_machine_type",
                args=[created_machine_type_info["id"]]
            ),
        )
        self.assertEqual(response.status_code, status.accepted)

    def test_create_update_and_list_machines(self):
        """Tests Creation, Update, Deletion and listing of the machines
        created.
        """
        # CREATE MACHINE TYPE
        msg = {
            "machine_type": ExistingMachineTypes.PI,
            "trained_employees": [self.admin_user.id],
        }
        response = self.client.post(
            reverse(viewname="create_machine_type"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)

        # taking the information from the created machine
        response_info = json.loads(response.content)
        created_machine_type_info = response_info["machine_type"]

        # CREATE MACHINE
        msg = {
            "machine_number": "1-1",
            "machine_title": "testing_machine",
            "machine_type": created_machine_type_info["id"],
        }
        response = self.client.post(
            reverse(viewname="create_machine"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)

        # taking the information from the created machine
        response_info = json.loads(response.content)
        created_machine_info = response_info["machine"]

        # LIST EXISTING MACHINES
        response = self.client.get(reverse(viewname="list_machines"))
        self.assertEqual(response.status_code, status.ok)

        # UPDATES MACHINE
        msg = {
            "machine_id": created_machine_info["id"], # ID from the created machine in the test
            "machine_number": "2-2",
            "machine_title": "testing_machine_update_test",
            # "machine_type": created_machine_type_info["id"],
        }

        response = self.client.post(
            reverse(viewname="update_machine"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.accepted)

        # DELETE MACHINE
        response = self.client.delete(
            reverse(viewname="delete_machine", args=[created_machine_info["id"]]),
        )
        self.assertEqual(response.status_code, status.accepted)
