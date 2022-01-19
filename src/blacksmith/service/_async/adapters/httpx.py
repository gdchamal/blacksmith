from typing import Mapping

import httpx
from httpx import Response as HttpxRepsonse
from httpx import Timeout as HttpxTimeout

from blacksmith.domain.exceptions import HTTPError, HTTPTimeoutError
from blacksmith.domain.model import HTTPRequest, HTTPResponse, HTTPTimeout
from blacksmith.service.ports import AsyncClient
from blacksmith.typing import ClientName, HttpMethod, Json, Path

from ..base import AsyncAbstractTransport


def safe_json(r: HttpxRepsonse) -> Json:
    try:
        return r.json()
    except Exception:
        return {"error": r.text}


class AsyncHttpxTransport(AsyncAbstractTransport):
    """
    Transport implemented using `httpx`_.

    .. _`httpx`: https://www.python-httpx.org/

    """

    async def __call__(
        self,
        req: HTTPRequest,
        method: HttpMethod,
        client_name: ClientName,
        path: Path,
        timeout: HTTPTimeout,
    ) -> HTTPResponse:
        headers = req.headers.copy()
        if req.body:
            headers["Content-Type"] = "application/json"
        async with AsyncClient(
            verify=self.verify_certificate,
            proxies=self.proxies,  # type: ignore
        ) as client:
            try:
                r = await client.request(  # type: ignore
                    method,
                    req.url,
                    params=req.querystring,
                    headers=headers,
                    content=req.body,
                    timeout=HttpxTimeout(timeout.request, connect=timeout.connect),
                )
            except httpx.TimeoutException as exc:
                raise HTTPTimeoutError(
                    f"{exc.__class__.__name__} while calling {method} {req.url}"
                )

        status_code: int = r.status_code  # type: ignore
        headers: Mapping[str, str] = r.headers  # type: ignore
        json = "" if status_code == 204 else safe_json(r)
        resp = HTTPResponse(status_code, headers, json=json)
        if not r.is_success:
            raise HTTPError(f"{r.status_code} {r.reason_phrase}", req, resp)
        return resp
