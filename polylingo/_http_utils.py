from __future__ import annotations

import httpx

from ._errors import AuthError, PolyLingoError, RateLimitError


def error_from_response(response: httpx.Response) -> PolyLingoError:
    try:
        data = response.json()
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    code = str(data.get("error", "unknown_error"))
    message = str(data.get("message", f"Request failed with status {response.status_code}"))
    status = response.status_code

    if status == 401:
        return AuthError(status, code, message)
    if status == 429:
        retry_raw = data.get("retry_after")
        retry_after: int | None
        if isinstance(retry_raw, int):
            retry_after = retry_raw
        elif isinstance(retry_raw, str) and retry_raw.isdigit():
            retry_after = int(retry_raw)
        else:
            retry_after = None
        if retry_after is None:
            h = response.headers.get("retry-after")
            if h and h.isdigit():
                retry_after = int(h)
        return RateLimitError(status, code, message, retry_after=retry_after)
    return PolyLingoError(status, code, message)
