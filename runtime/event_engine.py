from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from .store import MAXLegacyStore


@dataclass
class EventEngine:
    """Event engine that generates EV-xxxx ids and persists events via MAXLegacyStore."""

    store: MAXLegacyStore

    def next_event_id(self) -> str:
        """Return the next event id without persisting anything."""
        return self.store._next_event_id()

    def emit_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        event_id = self.store.save_event(event)
        event["id"] = event_id
        return event

    def emit_promotion_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.emit_event("promotion", payload)

    def emit_validation_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.emit_event("validation", payload)
