from __future__ import annotations


class PolyLingoError(Exception):
    """Base error for PolyLingo API failures."""

    def __init__(self, status: int, error: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.error = error


class AuthError(PolyLingoError):
    """Invalid or missing API key (HTTP 401)."""


class RateLimitError(PolyLingoError):
    """Rate limited (HTTP 429)."""

    def __init__(
        self,
        status: int,
        error: str,
        message: str,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(status, error, message)
        self.retry_after = retry_after


class JobFailedError(PolyLingoError):
    """Async job finished with status ``failed``."""

    def __init__(self, job_id: str, status: int, error: str, message: str) -> None:
        super().__init__(status, error, message)
        self.job_id = job_id
