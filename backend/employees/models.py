"""Employess Related models.
"""
from typing import (
    Any,
    Optional,
    Dict,
)
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from base.models import BaseModel


class RoleChoices(models.TextChoices):
    """TextChoices class to store the different roles currently on the app,
    where are defined both the value on the database and the human redable
    label.

    Example
    -------
    >>> employee = Employee.objects.get(identification=identification)
    >>> print(employee.role == RoleChoices.EMPLOYEE)
    """
    MANAGEMENT = "management", _("management")
    HR = "hr", _("human resources")
    QUALITY = "quality", _("quality")
    PRODUCTION_MANAGER = "prod_manager", _("production manager")
    PRODUCTION = "prod", _("production")
    ACCOUNTING = "accounting", _("accounting")


RoleChoices_dict = {value: label for value, label in RoleChoices.choices}

Role_list = [value for value, label in RoleChoices.choices]


class EmployessManager(BaseUserManager):
    """Custom user manager for the application.
    """
    def create_user(
        self,
        identification: str,
        names: str,
        last_names: str,
        birthday: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Optional[Dict[str, Any]]
    ):
        """Creates an Employee.
        """
        if not identification:
            raise ValueError(_("Employee must have an identification."))
        if not names:
            raise ValueError(_("Employee must have a name."))
        if not last_names:
            raise ValueError(_("Employee must have a last name."))
        if extra_fields.get("role") != RoleChoices.PRODUCTION and not password:
            raise ValueError(_("A password must be provided."))
        if extra_fields.get("role") == RoleChoices.PRODUCTION and password:
            raise ValueError(_("Production employees don't have password."))

        user = self.model(
            identification=identification,
            names=names,
            last_names=last_names,
            birthday=birthday,
            **extra_fields,
        )

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(
        self,
        identification: str,
        names: str,
        last_names: str,
        password: str,
        **extra_fields: Dict[str, Any]
    ):
        """Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("role", RoleChoices.MANAGEMENT)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("role") != RoleChoices.MANAGEMENT:
            raise ValueError(_("Superuser must have the management role."))

        user = self.create_user(
            identification=identification,
            names=names,
            last_names=last_names,
            password=password,
            birthday=None,
            **extra_fields
        )
        return user


class Employee(AbstractBaseUser, BaseModel):
    """Custom user model for the application.

    Parameters
    ----------
    identification: str
        Identification number of the Employee.
    names: str
        Names of the employee.
    last_names: str
        Last names of the employee.
    role: str
        Role of the employee.
    birthday: DateTime
        Date (DD/MM/YYYY) of the employee's birthday.
    """
    PRIVATE_FIELDS = [
        # "id",
        "trained_machines",
        "password",
        "is_active",
        "is_staff",
        "is_superuser",
    ]

    identification = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )
    names = models.CharField(
        max_length=100,
    )
    last_names = models.CharField(
        max_length=100,
    )
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.PRODUCTION,
    )
    birthday = models.DateField(
        blank=True,
        null=True,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        auto_now=True,
    )
    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=False,)
    is_superuser = models.BooleanField(default=False,)

    USERNAME_FIELD = "identification"
    REQUIRED_FIELDS = ["names", "last_names"]

    objects = EmployessManager()

    class Meta:
        db_table = "employees"
        indexes = [
            models.Index(fields=["identification"]),
        ]
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self):
        return f"{self.identification}, {self.role}"


class OOOTypes(models.TextChoices):
    """TextChoices class to store the different types of OOO currently on the
    app, where are defined both the value on the database and the human redable
    label.

    Example
    -------
    >>> employee_ooo = EmployeeOOO.objects.get(employee=employee)
    >>> print(employee_ooo.type)
    """
    PL = "paid_leave", _("paid leave")
    NPL = "non_paid_leave", _("non paid leave")
    WA = "work_accident", _("work accident")
    NWA = "non_work_accident", _("non_work_accident")
    PP = "paid_permit", _("paid permit")
    NPP = "non_paid_permit", _("non paid permit")


OOOTypes_dict = {value: label for value, label in OOOTypes.choices}


class OOO(BaseModel):
    """Out Of Office.

    Parameters
    ----------
    employee: Employee
        Employee that is OOO.
    ooo_type: str
        Type of OOO that the employee has.
    start_date: DateTime
        Date (HH:MM:SS DD/MM/YYYY) on which the OOO time starts.
    end_date: DateTime
        Date (HH:MM:SS DD/MM/YYYY) on which the OOO time ends.
    description: str
        Description of the OOO.
    """
    PRIVATE_FIELDS = [
        # "id",
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )
    ooo_type = models.CharField(
        max_length=20,
        choices=OOOTypes.choices,
        help_text=_("out of office time"),
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    class Meta:
        db_table = "ooo"
        verbose_name = "ooo"
        verbose_name_plural = "ooos"

    def __str__(self: "OOO") -> str:
        msg = (
            f"Employee: {self.employee}, "
            f"OOO type: {self.ooo_type}, "
            f"starting date: {self.start_date}, "
            f"ending date: {self.end_date}."
        )
        return msg
