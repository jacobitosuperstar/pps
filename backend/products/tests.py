import json
from django.test import TestCase, Client
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import RoleChoices, Employee
from products.models import Product


class ProductsWorkflowTest(TestCase):
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

    def test_create_update_and_list_products(self):
        """Tests Creation, Update, Deletion and listing of products.
        """
        # CREATE A PRODUCT
        msg = {
            "name": "Testing product 1",
            "materials": json.dumps({"testing_material_1": 1, "testing_material_2": 2}),
            # "materials": {"testing_material_1": 1, "testing_material_2": 2},
            # "materials": [1, 2, 3],
        }
        response = self.client.post(
            reverse(viewname="create_product"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)

        # taking the information from the created machine
        response_info = json.loads(response.content)
        created_product_info = response_info["product"]

        # LIST PRODUCTS
        response = self.client.get(reverse(viewname="list_products"))
        self.assertEqual(response.status_code, status.ok)
        response_info = json.loads(response.content)

        # DETAILED PRODUCT
        response = self.client.get(
            reverse(
                viewname="detailed_product",
                args=[created_product_info["id"]],
            )
        )
        self.assertEqual(response.status_code, status.accepted)

        # UPDATE PRODUCT
        msg = {
            "name": "Testing product 2",
            "materials": json.dumps({"testing_material_3": 3, "testing_material_4": 4}),
        }

        response = self.client.post(
            reverse(
                viewname="update_product",
                args=[created_product_info["id"]],
            ),
            data=msg,
        )
        self.assertEqual(response.status_code, status.accepted)

        # DELETE PRODUCT
        response = self.client.delete(
            reverse(
                viewname="delete_product",
                args=[created_product_info["id"]],
            )
        )
        self.assertEqual(response.status_code, status.accepted)

        # LIST PRODUCTS
        response = self.client.get(reverse(viewname="list_products"))
        self.assertEqual(response.status_code, status.ok)
