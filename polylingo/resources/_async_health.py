from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from polylingo._async_client import AsyncPolyLingo


async def health_async(client: AsyncPolyLingo) -> dict[str, object]:
    return await client._request_json("GET", "/health", expect_status=200)
