from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Optional


class WorkerRequest:
    """Minimal compatibility wrapper for Worker-style request access."""

    def __init__(self, method: str = "GET", url: str = "https://example.com", headers: Optional[Dict[str, str]] = None, body: Any = None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.body = body


class WorkerResponse:
    """Small response object that matches Cloudflare Worker behavior enough for tests."""

    def __init__(self, body: Any, status: int = 200, headers: Optional[Dict[str, str]] = None):
        self.status = status
        self.headers = headers or {}
        self.body = body

    def to_json(self) -> str:
        if isinstance(self.body, (dict, list, tuple)):
            return json.dumps(self.body)
        return str(self.body)


def worker_entry(request: WorkerRequest, env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> WorkerResponse:
    payload = {
        "status": "ok",
        "service": "max-legacy",
        "runtime": "cloudflare-worker",
        "method": getattr(request, "method", "GET"),
        "path": getattr(request, "url", "https://example.com").split("//", 1)[-1],
    }
    return WorkerResponse(payload, status=200, headers={"content-type": "application/json"})


def fetch(request: WorkerRequest, env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> WorkerResponse:
    return worker_entry(request=request, env=env, ctx=ctx)


def scheduled(event: Dict[str, Any], env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "max-legacy",
        "runtime": "cloudflare-worker",
        "event": event or {},
    }
