from rest_framework import serializers
from employees.models import Employee, RoleChoices, OOOTypes, OOO

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
        max_length=20,
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

class EmployeeOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'label']

    def get_label(self, obj):
        return f"{obj.names} {obj.last_names} - {obj.identification}"
        
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
    label = serializers.CharField()
    value = serializers.ChoiceField(
        choices=RoleChoices.choices,
    )

# OOO types serializer
class OOOTypesResponseSerializer(serializers.Serializer):
    """Serializer that returns a key-value dictionary of OOO types."""
    label = serializers.CharField()
    value = serializers.ChoiceField(
        choices=OOOTypes.choices,
    )

# OOO serializers
class OOOSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = OOO
        fields = ["id","employee", "ooo_type", "start_date", "end_date", "description"]


class CreateOOOSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=True,
    )
    ooo_type = serializers.ChoiceField(
        choices=OOOTypes.choices,
        required=True,
    )
    start_date = serializers.DateField(
        required=True,
    )
    end_date = serializers.DateField(
        required=True,
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    class Meta:
        model = OOO
        fields = ["employee", "ooo_type", "start_date", "end_date", "description"]


class UpdateOOOSerializer(serializers.ModelSerializer):
    ooo_type = serializers.ChoiceField(
        choices=OOOTypes.choices,
        required=True,
    )
    start_date = serializers.DateField(
        required=True,
    )
    end_date = serializers.DateField(
        required=True,
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    class Meta:
        model = OOO
        fields = ["ooo_type", "start_date", "end_date", "description"]
