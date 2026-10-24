"""Task queue implementation."""

from __future__ import annotations

from typing import Any, Dict, Optional


class TaskQueue:
    """Queue wrapper for general task scheduling."""

    def __init__(self, client: Optional[Any] = None, queue_name: str = "tasks"):
        self.client = client
        self.queue_name = queue_name

    def enqueue(self, task: Dict[str, Any], **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.publish(self.queue_name, task, **kwargs)

    def dequeue(self, **kwargs: Dict[str, Any]) -> Any:
        if self.client is None:
            raise RuntimeError("No queue client configured")
        return self.client.consume(self.queue_name, **kwargs)
