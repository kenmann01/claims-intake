# Confidential - Limited License, Author: Kanit Mann
"""JSONL record contract for run evidence: usage, output, and score rows,
plus append and load helpers shared by every runner."""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from promptlab.schemas import TaskName


class Record(BaseModel):
    """Base record: strict, unknown fields rejected."""
    model_config = ConfigDict(extra="forbid")


class UsageRecord(Record):
    """One model-call attempt projected onto the reporting contract."""
    run_id: str
    task: TaskName
    case_id: str
    model_name: str
    model_id: str
    prompt_id: str = ""
    prompt_version: str
    attempt: int
    kind: Literal["primary", "transport_retry", "repair", "repair_retry"]
    status: Literal["success", "schema_invalid", "transport_error"]
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    cost_usd: Decimal
    error: str | None = None


class OutputRecord(Record):
    """One case's schema-validation outcome and payload."""
    run_id: str
    task: TaskName
    case_id: str
    model_name: str
    model_id: str
    prompt_id: str = ""
    prompt_version: str
    succeeded: bool
    repairs: int
    output: dict[str, Any] | None
    error: str | None = None


class ScoreRecord(Record):
    """One scored metric row as a numerator and denominator."""
    run_id: str
    task: TaskName
    case_id: str
    model_name: str
    prompt_id: str = ""
    prompt_version: str
    scorer_version: str
    metric: str
    numerator: int
    denominator: int
    lower_is_better: bool = False
    detail: str | None = None


def append_record(path: Path, record: Record) -> None:
    """Append one record as a JSONL line, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(record.model_dump_json() + "\n")


def load_records[T: Record](path: Path, record_type: type[T]) -> list[T]:
    """Read records of the given type from JSONL; a missing file reads as empty."""
    if not path.exists():
        return []
    records: list[T] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(record_type.model_validate(json.loads(line)))
    return records

