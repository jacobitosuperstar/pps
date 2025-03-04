import json
from django.test import TestCase, Client
from django.test.client import WSGIRequest
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import RoleChoices, Employee, OOO, OOOTypes


class EmployeesWorkflowTest(TestCase):
    """Testing the CRUD of the Employees module
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
        self.admin_user.role = RoleChoices.HR
        self.admin_user.save()

        self.production_user = Employee.objects.create_user(
            identification="2222222222",
            names="test_production_employee",
            last_names="test_production_employee",
            role=RoleChoices.PRODUCTION,
        )

        msg = {
            "identification": "1111111111",
            "password": "AzQWsX09",
        }

        response = self.client.post(
            reverse(viewname="employees_login"),
            data=msg,
        )
        response = json.loads(response.content)
        token = response.get("token")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Token {token}"
        return

    def test_employee_roles(self):
        """Test to get all the employee roles
        """
        response = self.client.get(reverse(viewname="employees_roles"))
        self.assertEqual(response.status_code, status.ok)

    def test_get_list_of_empoloyees(self):
        """Test to get all the employess
        """
        response = self.client.get(reverse(viewname="employees"))
        self.assertEqual(response.status_code, status.ok)

    def test_get_list_of_filtered_empoloyees(self):
        """Test to get all the filtered employees.
        """
        response = self.client.get(
            reverse(viewname="employees_filtered"),
            data={"role": RoleChoices.PRODUCTION},
        )
        data = json.loads(response.content)
        for employee in data[Employee._meta.verbose_name_plural]:
            self.assertEqual(employee["role"], RoleChoices.PRODUCTION)
        self.assertEqual(response.status_code, status.ok)

    def test_employee_CRUD(self):
        """Test all the CRUD of an employee
        """
        # EMPLOYEE CREATION
        msg = {
            "identification": "3333333333",
            "names": "test_production_employee",
            "last_names": "test_production_employee",
            "role": RoleChoices.PRODUCTION,
        }
        response = self.client.post(
            reverse(viewname="employees"),
            data=msg,
        )
        data = json.loads(response.content)
        self.assertEqual(data["identification"], msg["identification"])
        self.assertEqual(response.status_code, status.created)

        # GETTING SPECIFIC EMPLOYEE
        response = self.client.get(
            reverse(
                viewname="employees_dud_employee",
                args=["3333333333"]
            ),
        )
        data = json.loads(response.content)
        self.assertEqual(
            data[Employee._meta.verbose_name]["identification"],
            msg["identification"]
        )
        self.assertEqual(response.status_code, status.ok)

        # UPDATING SPECIFIC EMPLOYEE
        msg = {
            "identification": "4444444444",
            "names": "test_updated_production_employee",
            "last_names": "test_updated_production_employee",
            "role": RoleChoices.PRODUCTION_MANAGER,
        }
        response = self.client.post(
            reverse(
                viewname="employees_dud_employee",
                args=["3333333333"]
            ),
            data=msg,
        )
        data = json.loads(response.content)
        self.assertEqual(
            data["identification"],
            msg["identification"]
        )
        self.assertEqual(
            data["role"],
            msg["role"]
        )
        self.assertEqual(response.status_code, status.accepted)

        # DELETING SPECIFIC EMPLOYEE
        response = self.client.delete(
            reverse(
                viewname="employees_dud_employee",
                args=["4444444444"]
            ),
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.accepted)


class OOOWorkflowTest(TestCase):
    """Testing the CRUD of the OOO module
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
        self.admin_user.role = RoleChoices.HR
        self.admin_user.save()

        self.production_user_1 = Employee.objects.create_user(
            identification="2222222222",
            names="test_production_employee_1",
            last_names="test_production_employee_1",
            role=RoleChoices.PRODUCTION,
        )

        self.production_user_2 = Employee.objects.create_user(
            identification="3333333333",
            names="test_production_employee_2",
            last_names="test_production_employee_2",
            role=RoleChoices.PRODUCTION,
        )

        self.ooo_1 = OOO.objects.create(
            employee=self.production_user_1,
            ooo_type=OOOTypes.PL,
            start_date="2100-01-07T07:30:00Z",
            end_date="2101-01-07T20:30:00Z",
            description="Nothing to see here, just normal paid time off.",
        )

        self.ooo_2 = OOO.objects.create(
            employee=self.production_user_2,
            ooo_type=OOOTypes.NPL,
            start_date="2100-01-07T07:30:00Z",
            end_date="2101-01-07T20:30:00Z",
            description="Nothing to see here, just normal paid time off.",
        )

        msg = {
            "identification": "1111111111",
            "password": "AzQWsX09",
        }

        response = self.client.post(
            reverse(viewname="employees_login"),
            data=msg,
        )
        response = json.loads(response.content)
        token = response.get("token")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Token {token}"
        return

    def test_employee_ooo_types(self):
        """Test to get all the employee roles
        """
        response = self.client.get(reverse(viewname="employees_ooo_types"))
        self.assertEqual(response.status_code, status.ok)

    def test_get_list_of_ooos(self):
        response = self.client.get(
            reverse(viewname="employees_ooos"),
        )
        data = json.loads(response.content)
        self.assertEqual(len(data[OOO._meta.verbose_name_plural]), 2)
        self.assertEqual(response.status_code, status.ok)

    def test_OOO_filtered_list(self):
        # filter by OOO type
        msg = {
            "ooo_type": OOOTypes.PL,
        }
        response = self.client.get(
            reverse(viewname="employees_filtered_ooo"),
            data=msg,
        )
        data = json.loads(response.content)
        for ooo in data[OOO._meta.verbose_name_plural]:
            self.assertEqual(ooo["ooo_type"], OOOTypes.PL)
        self.assertEqual(response.status_code, status.ok)

        # filter by employee
        msg = {
            "employee": "2222222222",
        }
        response = self.client.get(
            reverse(viewname="employees_filtered_ooo"),
            data=msg,
        )
        data = json.loads(response.content)
        for ooo in data[OOO._meta.verbose_name_plural]:
            self.assertEqual(ooo["employee"]["identification"], msg["employee"])
        self.assertEqual(response.status_code, status.ok)

    def test_ooo_detail(self):
        # GET OOO
        response = self.client.get(
            reverse(
                viewname="employees_dud_ooo",
                args=[self.ooo_1.id]
            ),
        )
        data = json.loads(response.content)
        self.assertEqual(
            data[OOO._meta.verbose_name]["employee"]["identification"],
            self.ooo_1.employee.identification,
        )
        self.assertEqual(response.status_code, status.ok)

    def test_OOO_creation(self):
        """Testing OOO Creation
        """
        # CREATE OOO
        msg = {
            "employee": "2222222222",
            "ooo_type": OOOTypes.PL,
            "start_date": "2100-01-07T07:30:00Z",
            "end_date": "2101-01-07T20:30:00Z",
            "description": "Nothing to see here, just normal paid time off.",
        }
        response = self.client.post(
            reverse(viewname="employees_ooos"),
            data=msg,
        )
        data = json.loads(response.content)
        self.assertEqual(
            data[OOO._meta.verbose_name]["ooo_type"],
            msg["ooo_type"],
        )
        self.assertEqual(
            data[OOO._meta.verbose_name]["employee"]["identification"],
            msg["employee"],
        )
        self.assertEqual(response.status_code, status.created)

    def test_OOO_update(self):
        """Testing OOO Update
        """
        # UPDATE OOO
        msg = {
            "employee": "3333333333",
            "ooo_type": OOOTypes.PL,
        }
        response = self.client.post(
            reverse(
                viewname="employees_dud_ooo",
                args=[self.ooo_2.id]
            ),
            data=msg,
        )
        data = json.loads(response.content)
        self.assertEqual(
            data[OOO._meta.verbose_name]["ooo_type"],
            msg["ooo_type"],
        )
        self.assertEqual(
            data[OOO._meta.verbose_name]["employee"]["identification"],
            msg["employee"],
        )
        self.assertEqual(response.status_code, status.accepted)

    def test_OOO_delete(self):
        """Testing OOO Delete
        """
        # DELETE OOO
        response = self.client.delete(
            reverse(
                viewname="employees_dud_ooo",
                args=[self.ooo_1.id]
            ),
        )
        self.assertEqual(response.status_code, status.accepted)
