from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Callable, Mapping, Optional

from polylingo._errors import JobFailedError

if TYPE_CHECKING:
    from polylingo._client import PolyLingo

DEFAULT_POLL_S = 5.0
DEFAULT_JOB_TIMEOUT_S = 1200.0  # 20 minutes (matches Node default)


class JobsResource:
    def __init__(self, client: PolyLingo) -> None:
        self._client = client

    def create(self, params: Mapping[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        p = _merge_params(params, kwargs)
        body = _job_body(p)
        return self._client._request_json("POST", "/jobs", json=body, expect_status=202)

    def get(self, job_id: str) -> dict[str, Any]:
        return self._client._request_json("GET", f"/jobs/{job_id}", expect_status=200)

    def translate(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        poll_interval: float = DEFAULT_POLL_S,
        timeout: float = DEFAULT_JOB_TIMEOUT_S,
        on_progress: Optional[Callable[[Optional[int]], None]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        p = _merge_params(params, kwargs)
        job = self.create(p)
        jid = str(job["job_id"])
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            status = self.get(jid)
            st = status.get("status")
            if st in ("pending", "processing") and on_progress is not None:
                on_progress(status.get("queue_position"))  # type: ignore[arg-type]
            if st == "completed":
                translations = status.get("translations")
                usage = status.get("usage")
                if not translations or not usage:
                    raise JobFailedError(
                        jid,
                        500,
                        "invalid_response",
                        "Job completed but translations or usage was missing",
                    )
                return {"translations": translations, "usage": usage}
            if st == "failed":
                raise JobFailedError(
                    jid,
                    200,
                    str(status.get("error") or "job_failed"),
                    str(status.get("message") or status.get("error") or "Translation job failed"),
                )
            time.sleep(poll_interval)

        raise JobFailedError(jid, 408, "timeout", "Job polling exceeded the configured timeout")


def _merge_params(
    params: Optional[Mapping[str, Any]],
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if params:
        out.update(dict(params))
    out.update(kwargs)
    return out


def _job_body(p: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "content": p["content"],
        "targets": p["targets"],
    }
    if p.get("format") is not None:
        body["format"] = p["format"]
    if p.get("source") is not None:
        body["source"] = p["source"]
    if p.get("model") is not None:
        body["model"] = p["model"]
    return body
