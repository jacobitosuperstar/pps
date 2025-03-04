"""JWT role validation mixins.
"""
from django.views import View

from jwt_authentication.decorators import authenticated_user
from .decorators import role_validation
from employees.models import RoleChoices


class AuthenticatedUserMixin(View):

    @classmethod
    def as_view(cls, **initkwargs):
        """We modify the creation of the view function from the View class and
        apply our function decorator to a method decorator with the
        `method_decorator` function. Then we apply it to the dispatch function
        so the decorator is executed before any request handling.
        """
        view = super().as_view(**initkwargs)
        # Apply authentication first
        view = authenticated_user(view=view)
        return view


class RoleValidatorMixin(AuthenticatedUserMixin):
    allowed_roles: list[RoleChoices] = []

    @classmethod
    def as_view(cls, **initkwargs):
        """We modify the creation of the view function from the View class and
        apply our function decorator to a method decorator with the
        `method_decorator` function. Then we apply it to the dispatch function
        so the decorator is executed before any request handling.
        """
        # calling the `as_view` function from the AuthenticatedUserMixin so
        # we don't have to validate authentication twice.
        view = super().as_view(**initkwargs)
        # Apply role validation after
        view = role_validation(allowed_roles=cls.allowed_roles,view=view)
        return view
