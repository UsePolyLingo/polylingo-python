from __future__ import annotations

from typing import Any, Literal, Optional, Union

import httpx

from polylingo._errors import PolyLingoError
from polylingo._http_utils import error_from_response
from polylingo.resources._async_batch import batch_async
from polylingo.resources._async_health import health_async
from polylingo.resources._async_jobs import AsyncJobsResource
from polylingo.resources._async_languages import languages_async
from polylingo.resources._async_translate import translate_async
from polylingo.resources._async_usage import usage_async

DEFAULT_BASE_URL = "https://api.usepolylingo.com/v1"

ExpectStatus = Union[int, tuple[int, ...]]


class AsyncPolyLingo:
    """Asynchronous PolyLingo API client."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 120.0,
    ) -> None:
        if not api_key or not isinstance(api_key, str):
            raise TypeError("AsyncPolyLingo: api_key is required")
        self._base = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self._base,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=httpx.Timeout(timeout),
        )
        self.jobs = AsyncJobsResource(self)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncPolyLingo:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        expect_status: Optional[ExpectStatus] = None,
    ) -> Any:
        try:
            response = await self._client.request(method, path, json=json)
        except httpx.TimeoutException:
            raise PolyLingoError(
                408,
                "timeout",
                f"Request timed out after {self._timeout}s",
            ) from None

        exp = expect_status
        if exp is None:
            ok = response.is_success
        elif isinstance(exp, tuple):
            ok = response.status_code in exp
        else:
            ok = response.status_code == exp

        if not ok:
            raise error_from_response(response)

        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    async def health(self) -> dict[str, Any]:
        return await health_async(self)

    async def languages(self) -> dict[str, Any]:
        return await languages_async(self)

    async def translate(
        self,
        *,
        content: str,
        targets: list[str],
        format: Optional[Literal["plain", "markdown", "json", "html"]] = None,
        source: Optional[str] = None,
        model: Optional[Literal["standard", "advanced"]] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"content": content, "targets": targets}
        if format is not None:
            params["format"] = format
        if source is not None:
            params["source"] = source
        if model is not None:
            params["model"] = model
        return await translate_async(self, params)

    async def batch(
        self,
        *,
        items: list[dict[str, Any]],
        targets: list[str],
        source: Optional[str] = None,
        model: Optional[Literal["standard", "advanced"]] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"items": items, "targets": targets}
        if source is not None:
            params["source"] = source
        if model is not None:
            params["model"] = model
        return await batch_async(self, params)

    async def usage(self) -> dict[str, Any]:
        return await usage_async(self)
