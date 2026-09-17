# Confidential - Limited License, Author: Kanit Mann
"""Shared adapter request/result types and the ModelAdapter protocol."""

from __future__ import annotations

from typing import Literal, Protocol

from pydantic import BaseModel

from promptlab.usage import CallRecord


class CompletionRequest(BaseModel):
    """One completion call: task identity, prompt layers, and sampling controls."""
    task: Literal["triage", "summarization", "extraction"]
    case_id: str
    prompt_id: str
    prompt_version: str
    system: str
    user_content: str
    temperature: float
    max_output_tokens: int


class CompletionResult(BaseModel):
    """Outcome of one adapter call plus every recorded attempt."""
    succeeded: bool
    text: str | None
    error_type: str | None
    records: list[CallRecord]


class ModelAdapter(Protocol):
    """Protocol every provider adapter must satisfy."""
    provider: str
    model_id: str

    def complete(self, request: CompletionRequest, run_id: str) -> CompletionResult:
        """Return the completion result for one request under the given run id."""
