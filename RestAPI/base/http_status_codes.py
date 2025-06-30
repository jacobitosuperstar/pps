from dataclasses import dataclass


@dataclass
class HTTP_STATUS:
    """Http Status Code."""
    ok: int = 200
    created: int = 201
    accepted: int = 202
    bad_request: int = 400
    unauthorized: int = 401
    forbidden: int = 403
    not_found: int = 404
    method_not_allowed: int = 405
    not_acceptable: int = 406
    im_a_teapot: int = 418
    internal_server_error: int = 500
