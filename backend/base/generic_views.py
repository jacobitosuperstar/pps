"""Base Mixins for the project.
"""
from typing import Any
from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpRequest
# from django.forms import ValidationError
from django.utils.translation import gettext as _
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)

from .models import BaseModel
from .response import ORJsonResponse as JsonResponse
from .logger import base_logger
from .http_status_codes import HTTP_STATUS as status

from .mixins import BaseMixin


class BaseListView(BaseMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base List Get View.
        Returns the total amount of objects given the GET request.
        """
        try:
            query_set: QuerySet[self.model] = self.filter_all_query()
            data: dict[str, dict[str, Any] | list[dict[str, Any]]] = {
                    self.model._meta.verbose_name_plural: self.serialize(query_set),
            }
            return JsonResponse(data, status=status.ok)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseFileteredListView(BaseMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base List Get View.
        Returns the list of the objects given the information in the GET
        request.
        """
        try:
            form_data: dict[str, Any] = self.validate_form(request=request)
            query_set: QuerySet[self.model] = self.filter_query(data=form_data)
            data: dict[str, dict[str, Any] | list[dict[str, Any]]] = {
                    self.model._meta.verbose_name_plural: self.serialize(query_set),
            }
            return JsonResponse(data, status=status.ok)
        except NotImplementedError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.internal_server_error)
        except ValidationError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.bad_request)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseCreateView(BaseMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base Post View.
        Creates a db object given the form data in the POST request.
        """
        try:
            form_data: dict[str, Any] = self.validate_form(request=request)
            created_object: BaseModel = self.create_object(data=form_data)
            msg: dict[str, dict[str, Any] | list[dict[str, Any]]] = {
                self.model._meta.verbose_name: self.serialize(created_object),
            }
            return JsonResponse(msg, status=status.created)
        except NotImplementedError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.internal_server_error)
        except ValidationError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.bad_request)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseDetailView(BaseMixin, View):
    url_kwarg: str = "id"

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base Detailed Get View.
        Returns the db object given the url_kwarg identifier.
        """
        try:
            data: dict[str, Any] = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object: BaseModel = self.get_query(data=data)
            msg = {
                self.model._meta.verbose_name: self.serialize(db_object),
            }
            return JsonResponse(msg, status=status.ok)
        except MultipleObjectsReturned as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.internal_server_error)
        except ObjectDoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)


class BaseUpdateView(BaseMixin, View):
    url_kwarg: str = "id"

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base Update View.
        Updates the db object given the url_kwarg identifier and the form data
        in the POST request.
        """
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object = self.get_query(data=data)
            form_data = self.validate_form(request)
            db_object = self.update_object(db_object=db_object, data=form_data)
            msg = {
                self.model._meta.verbose_name: self.serialize(db_object),
            }
            return JsonResponse(msg, status=status.accepted)
        except ValidationError as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.bad_request)
        except MultipleObjectsReturned as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.internal_server_error)
        except ObjectDoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)

class BaseDeleteView(BaseMixin, View):
    url_kwarg: str = "id"

    def delete(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Base Delete View.
        Deletes the db object given the url_kwarg identifier.
        """
        try:
            data = {self.url_kwarg: self.kwargs.get(self.url_kwarg)}
            db_object = self.get_query(data=data)
            self.delete_object(db_object=db_object)
            msg = {
                "response": _(f"{self.model._meta.verbose_name} has been deleted.")
            }
            return JsonResponse(msg, status=status.accepted)
        except MultipleObjectsReturned as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.internal_server_error)
        except ObjectDoesNotExist as e:
            error_data = e.args[0]
            return JsonResponse(error_data, status=status.not_found)
        except Exception as e:
            error_data = {
                "response": _("Internal server error.")
            }
            base_logger.critical(e)
            return JsonResponse(error_data, status=status.internal_server_error)
