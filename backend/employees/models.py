"""Employess Related models.
"""
from typing import (
    Any,
    Optional,
    Dict,
)
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class RoleChoices(models.TextChoices):
    """TextChoices class to store the different roles currently on the app,
    where are defined both the value on the database and the human redable
    label.

    Example
    -------
    >>> employee = Employee.objects.get(identification=identification)
    >>> print(employee.role == RoleChoices.EMPLOYEE)
    """
    MANAGEMENT = "management", "management"
    HR = "hr", "human resources"
    QUALITY = "quality", "quality"
    PRODUCTION_MANAGER = "prod_manager", "production manager"
    PRODUCTION = "prod", "production"
    ACCOUNTING = "accounting", "accounting"


class EmployessManager(BaseUserManager):
    """Custom user manager for the application.
    """
    def create_user(
        self,
        identification: str,
        names: str,
        lastnames: str,
        password: str,
        birthday: Optional[str] = None,
        **extra_fields: Optional[Dict[str, Any]]
    ):
        """Creates an Employee.
        """
        if not identification:
            raise ValueError(_("Employee must have an identification."))
        if not names:
            raise ValueError(_("Employee must have a name."))
        if not lastnames:
            raise ValueError(_("Employee must have a last name."))
        if not password:
            raise ValueError(_('A password must be provided.'))

        user = self.model(
            identification=identification,
            names=names,
            lastnames=lastnames,
            birthday=birthday,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        identification: str,
        names: str,
        lastnames: str,
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
            identification,
            names,
            lastnames,
            password,
            **extra_fields
        )
        return user


class Employee(AbstractBaseUser):
    """Custom user model for the application.
    """
    identification = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("identification"),
        help_text=_("")
    )
    names = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("employee names"),
        help_text=_("employee's names")
    )
    last_names = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("employee last names"),
        help_text=_("employee's lastnames")
    )
    role = models.CharField(
        max_length=120,
        choices=RoleChoices,
        default=RoleChoices.PRODUCTION,
        verbose_name=_("role"),
        help_test=_("employee role"),
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
    is_admin = models.BooleanField(default=False,)

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
    PL = "paid_leave", "paid leave"
    NPL = "non_paid_leave", "non paid leave"
    WA = "work_accident", "work accident"
    NWA = "non_work_accident", "non_work_accident"
    PP = "paid_permit", "paid permit"
    NPP = "non_paid_permit", "non paid permit"


class OOO(models.Model):
    """Employee type of OOO.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name=_("employee"),
    )
    ooo_type = models.CharField(
        max_length=50,
        choices=OOOTypes,
        blank=False,
        null=False,
        verbose_name=_("out of office"),
        help_test=_("out of office time"),
    )
    start_date = models.DateField(
        blank=False,
        null=False,
    )
    end_date = models.DateField(
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "ooo"
        verbose_name = ("out of office")
        verbose_name_plural = ("out of office")

    def __str__(self):
        msg = (
            f"Employee: {self.employee}, "
            f"OOO type: {self.ooo_type}, "
            f"starting date: {self.start_date}, "
            f"ending date: {self.end_date}."
        )
