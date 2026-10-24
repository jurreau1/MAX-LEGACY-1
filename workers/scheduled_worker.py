from __future__ import annotations

from typing import Any, Dict, Optional

from workers.api_worker import WorkerResponse, scheduled


def handle_scheduled(event: Dict[str, Any], env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return scheduled(event=event, env=env, ctx=ctx)


def scheduled_worker(event: Dict[str, Any], env: Optional[Dict[str, Any]] = None, ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return handle_scheduled(event=event, env=env, ctx=ctx)
