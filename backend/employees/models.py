"""Employess Related models.
"""
from typing import (
    Any,
    Optional,
    Dict,
)
from django.utils.translation import gettext as _
from django.utils import timezone
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
            raise ValueError(_('A password must be provided.'))

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
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("identification"),
        help_text=_("identification number")
    )
    names = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("employee names"),
        help_text=_("employee's names")
    )
    last_names = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("employee last names"),
        help_text=_("employee's lastnames")
    )
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.PRODUCTION,
        verbose_name=_("role"),
        help_text=_("employee role"),
    )
    birthday = models.DateField(
        blank=False,
        null=True,
        verbose_name=_("birthday"),
        help_text=_("birthday of the employee")
    )
    date_joined = models.DateField(
        auto_now_add=True,
        verbose_name=_("Joining date"),
    )
    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Login"),
    )
    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=False,)
    is_superuser = models.BooleanField(default=False,)

    USERNAME_FIELD = "identification"
    REQUIRED_FIELDS = ["names", "last_names"]

    objects = EmployessManager()

    class Meta:
        db_table = "employees"
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

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
    """Employee type of OOO.
    """
    PRIVATE_FIELDS = [
        # "id",
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("employee"),
    )
    ooo_type = models.CharField(
        max_length=20,
        choices=OOOTypes.choices,
        blank=False,
        null=False,
        verbose_name=_("out of office"),
        help_text=_("out of office time"),
    )
    start_date = models.DateTimeField(
        blank=False,
        null=False,
    )
    end_date = models.DateTimeField(
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "ooo"
        verbose_name = _("out of office")
        verbose_name_plural = _("out of office")

    def __str__(self: "OOO") -> str:
        msg = (
            f"Employee: {self.employee}, "
            f"OOO type: {self.ooo_type}, "
            f"starting date: {self.start_date}, "
            f"ending date: {self.end_date}."
        )
        return msg
