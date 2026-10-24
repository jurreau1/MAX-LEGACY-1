"""Metrics recording utilities."""

from __future__ import annotations

from typing import Any, Dict


class MetricsRecorder:
    """Minimal in-memory metrics recorder for worker applications."""

    def __init__(self):
        self._metrics: Dict[str, Any] = {}

    def increment(self, name: str, value: float = 1.0, **tags: Dict[str, str]) -> None:
        key = self._make_key(name, tags)
        self._metrics[key] = self._metrics.get(key, 0.0) + value

    def gauge(self, name: str, value: float, **tags: Dict[str, str]) -> None:
        key = self._make_key(name, tags)
        self._metrics[key] = value

    def get_metrics(self) -> Dict[str, Any]:
        return dict(self._metrics)

    @staticmethod
    def _make_key(name: str, tags: Dict[str, str]) -> str:
        if not tags:
            return name
        tag_string = ",".join(f"{key}={value}" for key, value in sorted(tags.items()))
        return f"{name}{{{tag_string}}}"
