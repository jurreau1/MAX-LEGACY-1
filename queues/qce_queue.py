"""QCE queue implementation."""

from __future__ import annotations

from typing import Any, Dict, Optional


class QCEQueue:
    """Queue wrapper for QCE-related work items."""

    def __init__(self, client: Optional[Any] = None, queue_name: str = "qce"):
        self.client = client
        self.queue_name = queue_name

    def enqueue(self, payload: Dict[str, Any], **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.publish(self.queue_name, payload, **kwargs)

    def dequeue(self, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.consume(self.queue_name, **kwargs)
