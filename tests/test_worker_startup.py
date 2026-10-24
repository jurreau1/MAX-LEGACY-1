from __future__ import annotations

from workers.api_worker import WorkerRequest, fetch


def test_worker_loads_and_registers_fetch_handler():
    import workers.api_worker as api_worker

    assert hasattr(api_worker, "fetch")
    assert callable(api_worker.fetch)


def test_worker_returns_http_response_for_health_route():
    request = WorkerRequest(method="GET", url="https://example.com/health")
    response = fetch(request=request)

    assert response.status == 200
    assert response.headers.get("content-type") == "application/json"
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["route"] == "/health"
    assert payload["service"] == "max-legacy"
