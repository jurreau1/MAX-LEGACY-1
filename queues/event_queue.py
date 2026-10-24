"""Event queue implementation."""

from __future__ import annotations

from typing import Any, Dict, Optional


class EventQueue:
    """Simple event queue abstraction used by workers."""

    def __init__(self, client: Optional[Any] = None, queue_name: str = "events"):
        self.client = client
        self.queue_name = queue_name

    def publish(self, event: Dict[str, Any], **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.publish(self.queue_name, event, **kwargs)

    def consume(self, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.consume(self.queue_name, **kwargs)
