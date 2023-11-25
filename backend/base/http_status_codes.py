from dataclasses import dataclass


@dataclass
class HTTP_STATUS:
    """Http Status Code."""
    ok = 200
    created = 201
    accepted = 202
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    not_acceptable = 406
    im_a_teapot = 418
    internal_server_error = 500
