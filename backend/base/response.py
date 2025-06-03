from django.http import (
    HttpResponse,
)
import orjson as json


class ORJsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON using
    the fast orjson library.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before ECMAScript 5. See
      the ``safe`` parameter for more information.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    """

    def __init__(
        self,
        data,
        safe=True,
        **kwargs,
    ):
        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        kwargs.setdefault("content_type", "application/json")
        data = json.dumps(data)
        super().__init__(content=data, **kwargs)
