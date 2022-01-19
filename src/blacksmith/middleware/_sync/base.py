from typing import Dict

from blacksmith.domain.model.http import HTTPRequest, HTTPResponse, HTTPTimeout
from blacksmith.domain.typing import SyncMiddleware
from blacksmith.typing import ClientName, HttpMethod, Path


class SyncHTTPMiddleware:
    """Inject data in http query on every requests."""

    def __init__(self) -> None:
        pass

    def initialize(self) -> None:
        pass

    def __call__(self, next: SyncMiddleware) -> SyncMiddleware:
        def handle(
            req: HTTPRequest,
            method: HttpMethod,
            client_name: ClientName,
            path: Path,
            timeout: HTTPTimeout,
        ) -> HTTPResponse:
            return next(req, method, client_name, path, timeout)

        return handle


class SyncHTTPAddHeadersMiddleware(SyncHTTPMiddleware):
    """
    Generic middleware that inject HTTP headers.

    :params: headers to inject in HTTP requests.
    """

    headers: Dict[str, str]

    def __init__(self, headers: Dict[str, str]):
        self.headers = headers

    def __call__(self, next: SyncMiddleware) -> SyncMiddleware:
        def handle(
            req: HTTPRequest,
            method: HttpMethod,
            client_name: ClientName,
            path: Path,
            timeout: HTTPTimeout,
        ) -> HTTPResponse:
            req.headers.update(self.headers)
            return next(req, method, client_name, path, timeout)

        return handle
