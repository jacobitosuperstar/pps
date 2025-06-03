"""Machinery related models.
"""
from typing import (
    Any,
    Optional,
    Dict,
    List,
)
from django.utils.translation import gettext as _
from django.db import models
from django.db.models import Q

from base.models import BaseModel
from employees.models import Employee, OOO


class ExistingMachineTypes(models.TextChoices):
    """TextChoices class to store the different types of machines currently on
    the factory, where are defined both the value on the database and the human
    redable label.

    Example
    -------
    >>> machine = MachineType.objects.get(id=id)
    >>> print(machine.machine_type)
    """
    PI = "plastic_inyector", _("plastic inyector")
    PE = "plastic_extruder", _("plastic extruder")


ExistingMachineTypes_dict: dict = {
    value: label for value, label
    in ExistingMachineTypes.choices
}


class MachineType(BaseModel):
    """The idea of this model is that there is only one type of machine and a
    lot of users can be trained to use them.

    Parameters
    ----------
    machine_type: str
        Type of Machine on which the employess are trained.
    trained_employees: Iterable[Employee]
        List of employees that are trained to use this machinery type.
    """
    machine_type = models.CharField(
        max_length=100,
        choices=ExistingMachineTypes.choices,
        unique=True,
    )
    trained_employees = models.ManyToManyField(
        to=Employee,
        related_name="trained_machines",
    )

    class Meta:
        db_table = "machine_type"
        verbose_name = "machine_type"
        verbose_name_plural = "machine_types"

    def __str__(self) -> str:
        msg = f"Machine Type: {self.machine_type}"
        return msg


class Machine(BaseModel):
    """These are the machines that physically are in the facility.

    Parameters
    ----------
    machine_numer: str
        Number like identifier of the machine.
    machine_title: str
        Name of the machine.
    machine_type: MachineType
        Machine type of this machine.
    """
    machine_number = models.CharField(
        max_length=100,
    )
    machine_title = models.CharField(
        max_length=100,
    )
    machine_type = models.ForeignKey(
        to=MachineType,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "machine"
        unique_together = ("machine_number", "machine_title")
        verbose_name = "machine"
        verbose_name_plural = "machines"

    def __str__(self) -> str:
        msg = f"Machine {self.machine_number}: {self.machine_title}"
        return msg

    def employees_to_assign(
        self,
        start_date: str,
        end_date: str,
    ) -> List[Optional[Dict[str, Any]]]:
        """Given a range of dates we can return all the employess that can be
        working on this particular machine instance.
        """
        # getting all the employees that are OOO
        ooo_employees = OOO.objects.filter(
            Q(start_date__lte=end_date)
            &
            Q(end_date__gte=start_date)
        ).values_list(
            "employee__id",
            flat=True,
        )

        # getting all the available trained employees
        available_trained_employess = (
            self.machine_type.trained_employees
            .exclude(
                id__in=ooo_employees
            )
            .values_list(
                "id",
                flat=True,
            )
        )

        employees = Employee.objects.filter(id__in=available_trained_employess)
        employees = [
            employee.serialize() for employee in employees
        ]
        return employees
