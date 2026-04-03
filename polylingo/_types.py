from __future__ import annotations

from typing import Any, Literal, TypedDict

ContentFormat = Literal["plain", "markdown", "json", "html"]
ModelTier = Literal["standard", "advanced"]
JobStatus = Literal["pending", "processing", "completed", "failed"]


class TranslateUsage(TypedDict, total=False):
    total_tokens: int
    input_tokens: int
    output_tokens: int
    model: str
    detected_format: str
    detection_confidence: float


class TranslateResult(TypedDict):
    translations: dict[str, str]
    usage: TranslateUsage


class BatchItem(TypedDict, total=False):
    id: str
    content: str
    format: ContentFormat
    source: str


class BatchItemResult(TypedDict):
    id: str
    translations: dict[str, str]


class BatchUsage(TypedDict, total=False):
    total_tokens: int
    input_tokens: int
    output_tokens: int
    model: str


class BatchResult(TypedDict):
    results: list[BatchItemResult]
    usage: BatchUsage


class Job(TypedDict, total=False):
    job_id: str
    status: JobStatus
    queue_position: int
    translations: dict[str, str]
    usage: TranslateUsage
    error: str
    message: str
    created_at: str
    updated_at: str
    completed_at: str | None


class HealthResponse(TypedDict):
    status: str
    timestamp: str


class LanguageEntry(TypedDict):
    code: str
    name: str


class LanguagesResponse(TypedDict):
    languages: list[LanguageEntry]


class UsagePayload(TypedDict, total=False):
    period_start: str
    period_end: str
    translations_used: int
    translations_limit: int | None
    tokens_used: int
    tokens_limit: int | None


class UsageResponse(TypedDict):
    usage: UsagePayload


# --- Params (plain dicts are fine; these document expected keys) ---


class TranslateParams(TypedDict, total=False):
    content: str
    targets: list[str]
    format: ContentFormat
    source: str
    model: ModelTier


class BatchParams(TypedDict, total=False):
    items: list[BatchItem]
    targets: list[str]
    source: str
    model: ModelTier


class CreateJobParams(TypedDict, total=False):
    content: str
    targets: list[str]
    format: ContentFormat
    source: str
    model: ModelTier


class JobsTranslateParams(CreateJobParams, total=False):
    poll_interval: float
    timeout: float
    on_progress: Any  # Callable[[int | None], None] — avoid circular import
