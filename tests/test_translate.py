import pytest


def test_translate_posts_json(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/translate",
        status_code=200,
        json={
            "translations": {"es": "Hola"},
            "usage": {"total_tokens": 3, "input_tokens": 1, "output_tokens": 2},
        },
    )
    from polylingo import PolyLingo

    client = PolyLingo("secret", base_url="https://api.example.com/v1")
    r = client.translate(content="Hi", targets=["es"], format="plain")
    assert r["translations"]["es"] == "Hola"
    req = httpx_mock.get_request()
    assert req.headers["Authorization"] == "Bearer secret"
    import json

    body = json.loads(req.content.decode())
    assert body == {"content": "Hi", "targets": ["es"], "format": "plain"}


@pytest.mark.asyncio
async def test_async_translate(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/translate",
        status_code=200,
        json={"translations": {"de": "Ja"}, "usage": {"total_tokens": 1, "input_tokens": 0, "output_tokens": 1}},
    )
    from polylingo import AsyncPolyLingo

    async with AsyncPolyLingo("x", base_url="https://api.example.com/v1") as c:
        r = await c.translate(content="Yes", targets=["de"])
    assert r["translations"]["de"] == "Ja"
