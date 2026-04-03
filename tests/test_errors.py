import pytest

from polylingo import AsyncPolyLingo, AuthError, PolyLingo, RateLimitError


def test_auth_error_on_401(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/translate",
        status_code=401,
        json={"error": "invalid_api_key", "message": "Bad"},
    )
    client = PolyLingo("k", base_url="https://api.example.com/v1")
    with pytest.raises(AuthError):
        client.translate(content="hi", targets=["es"])


def test_rate_limit_retry_after_header(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/translate",
        status_code=429,
        json={"error": "rate_limited", "message": "Slow"},
        headers={"Retry-After": "60"},
    )
    client = PolyLingo("k", base_url="https://api.example.com/v1")
    with pytest.raises(RateLimitError) as ei:
        client.translate(content="hi", targets=["es"])
    assert ei.value.retry_after == 60


@pytest.mark.asyncio
async def test_async_auth_error(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/translate",
        status_code=401,
        json={"error": "invalid_api_key", "message": "Bad"},
    )
    async with AsyncPolyLingo("k", base_url="https://api.example.com/v1") as c:
        with pytest.raises(AuthError):
            await c.translate(content="hi", targets=["es"])
