from __future__ import annotations

from typing import Any, Dict, Optional

from workers.api_worker import WorkerRequest, WorkerResponse, fetch, scheduled


def handle_event(event: Dict[str, Any], env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = {
        "status": "ok",
        "service": "max-legacy",
        "runtime": "cloudflare-worker",
        "event": event or {},
    }
    return payload


def event_handler(event: Dict[str, Any], env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return handle_event(event=event, env=env, ctx=ctx)


def handle_request(request: WorkerRequest, env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> WorkerResponse:
    return fetch(request=request, env=env, ctx=ctx)
