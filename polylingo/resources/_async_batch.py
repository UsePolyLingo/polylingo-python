from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from polylingo._async_client import AsyncPolyLingo


async def batch_async(client: AsyncPolyLingo, params: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "items": params["items"],
        "targets": params["targets"],
    }
    if params.get("source") is not None:
        body["source"] = params["source"]
    if params.get("model") is not None:
        body["model"] = params["model"]
    return await client._request_json("POST", "/translate/batch", json=body, expect_status=200)
