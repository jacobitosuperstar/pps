import json
from django.test import TestCase, Client
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status
from employees.models import RoleChoices, Employee
from products.models import Product


class ProductsUnitTest(TestCase):
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

        self.product

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

    def test_create_product(self):
        """Test Creation of a product
        """
        # CREATE A PRODUCT
        msg = {
            "name": "Testing product 1",
            "materials": json.dumps({"testing_material_1": 1, "testing_material_2": 2}),
        }
        response = self.client.post(
            reverse(viewname="products"),
            data=msg,
        )
        data = json.loads(response.content)
        created_product = data[Product._meta.verbose_name]
        self.assertEqual(
            created_product["name"],
            msg["name"],
        )
        self.assertEqual(
            created_product["materials"],
            msg["materials"],
        )
        self.assertEqual(response.status_code, status.created)

        # LIST PRODUCTS
        response = self.client.get(reverse(viewname="products"))
        data = json.loads(response.content)
        products_list = [
            product["id"] for product
            in data[Product._meta.verbose_name_plural]
        ]
        self.assertTrue(
            created_product["id"] in products_list,
            "The created product is not in the products list."
        )
        self.assertEqual(response.status_code, status.ok)

        # DETAILED PRODUCT
        response = self.client.get(
            reverse(
                viewname="products_dud",
                args=[created_product["id"]],
            )
        )
        data = json.loads(response.content)
        product = data[Product._meta.verbose_name]
        self.assertEqual(
            created_product["name"],
            product["name"],
        )
        self.assertEqual(
            created_product["materials"],
            product["materials"],
        )
        self.assertEqual(response.status_code, status.accepted)

        # UPDATE PRODUCT
        msg = {
            "name": "Testing product 2",
            "materials": json.dumps({"testing_material_3": 3, "testing_material_4": 4}),
        }

        response = self.client.post(
            reverse(
                viewname="products_dud",
                args=[created_product["id"]],
            ),
            data=msg,
        )
        self.assertEqual(response.status_code, status.accepted)

        # DELETE PRODUCT
        response = self.client.delete(
            reverse(
                viewname="products_dud",
                args=[created_product_info["id"]],
            )
        )
        self.assertEqual(response.status_code, status.accepted)
