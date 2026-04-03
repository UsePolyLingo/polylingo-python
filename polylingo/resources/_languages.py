from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from polylingo._client import PolyLingo


def languages(client: PolyLingo) -> dict[str, object]:
    return client._request_json("GET", "/languages", expect_status=200)
