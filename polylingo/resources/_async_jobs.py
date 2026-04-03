from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any, Callable, Mapping, Optional

from polylingo._errors import JobFailedError
from polylingo.resources._jobs import DEFAULT_JOB_TIMEOUT_S, DEFAULT_POLL_S, _job_body, _merge_params

if TYPE_CHECKING:
    from polylingo._async_client import AsyncPolyLingo


class AsyncJobsResource:
    def __init__(self, client: AsyncPolyLingo) -> None:
        self._client = client

    async def create(self, params: Mapping[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        p = _merge_params(params, kwargs)
        body = _job_body(p)
        return await self._client._request_json("POST", "/jobs", json=body, expect_status=202)

    async def get(self, job_id: str) -> dict[str, Any]:
        return await self._client._request_json("GET", f"/jobs/{job_id}", expect_status=200)

    async def translate(
        self,
        params: Mapping[str, Any] | None = None,
        *,
        poll_interval: float = DEFAULT_POLL_S,
        timeout: float = DEFAULT_JOB_TIMEOUT_S,
        on_progress: Optional[Callable[[Optional[int]], None]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        p = _merge_params(params, kwargs)
        job = await self.create(p)
        jid = str(job["job_id"])
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            status = await self.get(jid)
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
            await asyncio.sleep(poll_interval)

        raise JobFailedError(jid, 408, "timeout", "Job polling exceeded the configured timeout")
