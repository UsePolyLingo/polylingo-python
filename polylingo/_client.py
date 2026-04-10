from __future__ import annotations

from typing import Any, Literal, Optional, Union

import httpx

from polylingo._errors import PolyLingoError
from polylingo._http_utils import error_from_response
from polylingo.resources._batch import batch
from polylingo.resources._health import health
from polylingo.resources._jobs import JobsResource
from polylingo.resources._languages import languages
from polylingo.resources._translate import translate
from polylingo.resources._usage import usage

DEFAULT_BASE_URL = "https://api.usepolylingo.com/v1"

ExpectStatus = Union[int, tuple[int, ...]]


class PolyLingo:
    """Synchronous PolyLingo API client."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 120.0,
    ) -> None:
        if not api_key or not isinstance(api_key, str):
            raise TypeError("PolyLingo: api_key is required")
        self._base = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._client = httpx.Client(
            base_url=self._base,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=httpx.Timeout(timeout),
        )
        self.jobs = JobsResource(self)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> PolyLingo:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        expect_status: Optional[ExpectStatus] = None,
    ) -> Any:
        try:
            response = self._client.request(method, path, json=json)
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

    def health(self) -> dict[str, Any]:
        return health(self)

    def languages(self) -> dict[str, Any]:
        return languages(self)

    def translate(
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
        return translate(self, params)

    def batch(
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
        return batch(self, params)

    def usage(self) -> dict[str, Any]:
        return usage(self)
