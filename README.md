# polylingo (Python)

Official Python SDK for the [PolyLingo](https://usepolylingo.com) translation API.

**Requirements:** Python 3.9+

## Install

```bash
pip install polylingo
```

## Sync usage

```python
import os
import polylingo

client = polylingo.PolyLingo(
    api_key=os.environ["POLYLINGO_API_KEY"],
    # base_url="https://api.polylingo.io/v1",
    # timeout=120.0,
)

result = client.translate(content="# Hello", targets=["es", "fr"], format="markdown")
print(result["translations"]["es"])
client.close()
```

Context manager:

```python
with polylingo.PolyLingo(api_key="...") as client:
    print(client.languages())
```

## Async usage

```python
import polylingo

async with polylingo.AsyncPolyLingo(api_key="...") as client:
    r = await client.translate(content="Hi", targets=["de"])
```

## API

- `health()` / `await health()`
- `languages()`
- `translate(content=..., targets=..., format=..., source=..., model=...)`
- `batch(items=..., targets=..., source=..., model=...)`
- `usage()`
- `jobs.create(...)` — returns 202 payload
- `jobs.get(job_id)`
- `jobs.translate(..., poll_interval=5.0, timeout=1200.0, on_progress=...)`

## Exceptions

- `PolyLingoError` — base (`status`, `error`, `args[0]` message)
- `AuthError` — 401
- `RateLimitError` — 429 (`retry_after`)
- `JobFailedError` — failed job (`job_id`)

## Docs

[Python SDK reference](https://usepolylingo.com/en/docs/sdk/python) (when deployed).

## Repository

[UsePolyLingo/polylingo-python](https://github.com/UsePolyLingo/polylingo-python)

## License

MIT
