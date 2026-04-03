# polylingo (Python)

Python client for the [PolyLingo](https://usepolylingo.com) translation API.

Requires Python 3.9+.

## Install

```bash
pip install polylingo
```

## Sync client

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

```python
with polylingo.PolyLingo(api_key="...") as client:
    print(client.languages())
```

## Async client

```python
import polylingo

async with polylingo.AsyncPolyLingo(api_key="...") as client:
    r = await client.translate(content="Hi", targets=["de"])
```

## API

Same names on `PolyLingo` and `AsyncPolyLingo` (async methods are awaited).

| Area | Notes |
|------|--------|
| `health()` | `GET /health` |
| `languages()` | `GET /languages` |
| `translate(...)` | `POST /translate` |
| `batch(...)` | `POST /translate/batch` |
| `usage()` | `GET /usage` |
| `jobs.create(...)` | `POST /jobs` (202 body) |
| `jobs.get(job_id)` | `GET /jobs/:id` |
| `jobs.translate(...)` | Submit and poll (`poll_interval`, `timeout`, `on_progress`) |

## Exceptions

`PolyLingoError` (`status`, `error`, message string). `AuthError` (401), `RateLimitError` (429, `retry_after`), `JobFailedError` (`job_id`).

## Documentation

[Python SDK on usepolylingo.com](https://usepolylingo.com/en/docs/sdk/python)

## Repository

[github.com/UsePolyLingo/polylingo-python](https://github.com/UsePolyLingo/polylingo-python)

## License

MIT
