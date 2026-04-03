import pytest

from polylingo import JobFailedError, PolyLingo


def test_jobs_translate_completed(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/jobs",
        status_code=202,
        json={"job_id": "j1", "status": "pending"},
    )
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/v1/jobs/j1",
        status_code=200,
        json={
            "job_id": "j1",
            "status": "completed",
            "translations": {"fr": "Salut"},
            "usage": {"total_tokens": 2, "input_tokens": 1, "output_tokens": 1},
        },
    )
    client = PolyLingo("k", base_url="https://api.example.com/v1")
    done = client.jobs.translate(content="Hi", targets=["fr"], poll_interval=0.01, timeout=5.0)
    assert done["translations"]["fr"] == "Salut"


def test_jobs_translate_failed(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/v1/jobs",
        status_code=202,
        json={"job_id": "j1", "status": "pending"},
    )
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/v1/jobs/j1",
        status_code=200,
        json={"job_id": "j1", "status": "failed", "error": "boom"},
    )
    client = PolyLingo("k", base_url="https://api.example.com/v1")
    with pytest.raises(JobFailedError) as ei:
        client.jobs.translate(content="x", targets=["de"], poll_interval=0.01, timeout=5.0)
    assert ei.value.job_id == "j1"
