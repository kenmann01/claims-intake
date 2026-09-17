# Confidential - Limited License, Author: Kanit Mann
"""The thinking-mode toggle stays behind the adapter and follows config."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
import pytest

from promptlab.adapters.base import CompletionRequest
from promptlab.adapters.ollama import OllamaAdapter
from promptlab.config import Settings


def _request() -> CompletionRequest:
    """Build a minimal summarization request for adapter calls."""
    return CompletionRequest(
        task="summarization",
        case_id="case_001",
        prompt_id="baseline",
        prompt_version="v0",
        system="system",
        user_content="user",
        temperature=0.0,
        max_output_tokens=64,
    )


class FakeResponse:
    """Minimal stand-in for an httpx.Response."""
    def __init__(self) -> None:
        """Pin the success status code."""
        self.status_code = 200

    def json(self) -> dict[str, Any]:
        """Return a minimal successful Ollama payload."""
        return {
            "response": "ok",
            "prompt_eval_count": 1,
            "eval_count": 1,
            "done_reason": "stop",
        }


def test_qwen_thinking_defaults_to_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without env overrides, qwen thinking is off and mistral unset."""
    monkeypatch.delenv("MODEL_A_THINK", raising=False)
    monkeypatch.delenv("MODEL_B_THINK", raising=False)
    settings = Settings.from_env()
    assert settings.models["qwen"].think is False
    assert settings.models["mistral"].think is None


def test_thinking_flag_follows_model_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The request body carries think only when config fixes it."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MODEL_A_THINK", raising=False)
    monkeypatch.delenv("MODEL_B_THINK", raising=False)
    captured: dict[str, dict[str, Any]] = {}

    def fake_post(url: str, json: dict[str, Any], **kwargs: Any) -> FakeResponse:
        """Capture request bodies by model and answer with success."""
        captured[json["model"]] = json
        return FakeResponse()

    monkeypatch.setattr(httpx, "post", fake_post)

    settings = Settings.from_env()
    for logical, config in settings.models.items():
        adapter = OllamaAdapter(model_id=config.model_id)
        adapter.complete(_request(), "thinking-run")
        body = captured[config.model_id]
        if config.think is None:
            assert "think" not in body, logical
        else:
            assert body["think"] is config.think, logical
