from __future__ import annotations

import tomllib
from pathlib import Path


def test_cloudflare_worker_configuration():
    root = Path(__file__).resolve().parents[1]
    config_paths = [root / "wrangler.toml", root / "cloudflare" / "wrangler.toml"]

    found = None
    for path in config_paths:
        if path.exists():
            found = path
            break

    assert found is not None, "Expected a Wrangler configuration for a Cloudflare Worker deployment."

    data = tomllib.loads(found.read_text(encoding="utf-8"))
    assert data["name"] == "max-legacy"
    assert data["main"].endswith("workers/api_worker.py")
    assert "python_workers" in data.get("compatibility_flags", [])
    assert data.get("workers_dev") is True
    assert "pages_build_output_dir" not in data
    assert "[site]" not in found.read_text(encoding="utf-8")


def test_worker_entrypoints_exist():
    root = Path(__file__).resolve().parents[1]
    api = root / "workers" / "api_worker.py"
    event = root / "workers" / "event_worker.py"
    scheduled = root / "workers" / "scheduled_worker.py"

    assert api.exists()
    assert event.exists()
    assert scheduled.exists()

    import importlib

    api_mod = importlib.import_module("workers.api_worker")
    event_mod = importlib.import_module("workers.event_worker")
    scheduled_mod = importlib.import_module("workers.scheduled_worker")

    assert hasattr(api_mod, "fetch")
    assert hasattr(event_mod, "event_handler")
    assert hasattr(scheduled_mod, "handle_scheduled")


def test_worker_startup_success():
    from workers.api_worker import WorkerRequest, fetch

    request = WorkerRequest(method="GET", url="https://example.com/healthz")
    response = fetch(request=request)

    assert response.status == 200
    payload = response.to_json()
    assert "cloudflare-worker" in payload
    assert "max-legacy" in payload
