from rest_framework import serializers
from employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'identification',
            'names',
            'last_names',
            'role',
            'birthday',
        ]

class EmployeeAuthenticationSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

class EmployeeLoginResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    employee = EmployeeSerializer()
    token = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    errors = serializers.JSONField()

class RoleChoicesResponseSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of available roles for employees."
    )