"""Audit logging utilities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class AuditLogger:
    """Lightweight audit logger for worker events."""

    def __init__(self, sink: Any = None):
        self.sink = sink

    def log(self, action: str, **fields: Dict[str, Any]) -> Dict[str, Any]:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            **fields,
        }
        if self.sink is not None:
            self.sink(record)
        return record
