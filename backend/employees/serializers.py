from rest_framework import serializers
from employees.models import Employee, RoleChoices

# Commons
class CommonFilterSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    page_size = serializers.IntegerField(required=False, min_value=1, default=10)
    search = serializers.CharField(required=False, max_length=100, default="")
class ErrorResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    errors = serializers.JSONField()

# Employee serializers
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            'identification',
            'names',
            'last_names',
            'role',
            'birthday',
        ]

class CreateEmployeeSerializer(serializers.ModelSerializer):
    identification = serializers.CharField(
        max_length=50,
        required=True,
    )
    names = serializers.CharField(
        max_length=100,
        required=True,
    )
    last_names = serializers.CharField(
        max_length=100,
        required=True,
    )
    birthday = serializers.DateField(
        required=False,
    )
    role = serializers.ChoiceField(
        choices=RoleChoices.choices,
        initial=RoleChoices.PRODUCTION,
        required=True,
    )

    class Meta:
        model = Employee
        fields = ["identification", "names", "last_names", "role", "birthday"]
class UpdateEmployeeSerializer(serializers.ModelSerializer):
    names = serializers.CharField(
        max_length=100,
        required=True,
    )
    last_names = serializers.CharField(
        max_length=100,
        required=True,
    )
    birthday = serializers.DateField(
        required=False,
    )
    role = serializers.ChoiceField(
        choices=RoleChoices.choices,
        initial=RoleChoices.PRODUCTION,
        required=True,
    )

    class Meta:
        model = Employee
        fields = ["names", "last_names", "role", "birthday"]
        
# Login serializer for employees
class EmployeeAuthenticationSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

class EmployeeLoginResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    employee = EmployeeSerializer()
    token = serializers.CharField()

# Role choices serializer
class RoleChoicesResponseSerializer(serializers.Serializer):
    types = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of available roles for employees."
    )

# OOO types serializer
class OOOTypesResponseSerializer(serializers.Serializer):
    """Serializer that returns a key-value dictionary of OOO types."""
    types = serializers.ListField(
        child=serializers.CharField(),
        help_text="Dictionary of OOO types with their human-readable labels."
    )

class EmployeeResponseSerializer(serializers.Serializer):
    """Serializer for employee creation response."""
    identification = serializers.CharField()
    role = serializers.ChoiceField(choices=RoleChoices.choices)
    generated_password = serializers.CharField(required=False)
