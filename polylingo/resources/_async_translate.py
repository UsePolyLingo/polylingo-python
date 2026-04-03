from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from polylingo._async_client import AsyncPolyLingo


async def translate_async(client: AsyncPolyLingo, params: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "content": params["content"],
        "targets": params["targets"],
    }
    if params.get("format") is not None:
        body["format"] = params["format"]
    if params.get("source") is not None:
        body["source"] = params["source"]
    if params.get("model") is not None:
        body["model"] = params["model"]
    return await client._request_json("POST", "/translate", json=body, expect_status=200)
