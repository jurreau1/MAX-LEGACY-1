import os
import shutil
from pathlib import Path

from runtime.store import MAXLegacyStore


def test_save_and_load_knowledge(tmp_path: Path):
    # Use a temporary copy of the repository layout to avoid polluting the repo in CI
    repo_tmp = tmp_path / "repo"
    repo_tmp.mkdir()
    (repo_tmp / "knowledge").mkdir()
    (repo_tmp / "events").mkdir()

    store = MAXLegacyStore(root=repo_tmp)

    k = {"title": "K-001 title", "content": "hello"}
    k_id = store.save_knowledge(k)
    assert k_id.startswith("K-")

    loaded = store.load_knowledge(k_id)
    assert loaded["id"] == k_id
    assert loaded["title"] == "K-001 title"

    listed = store.list_knowledge()
    assert k_id in listed


def test_save_and_load_event(tmp_path: Path):
    repo_tmp = tmp_path / "repo"
    repo_tmp.mkdir()
    (repo_tmp / "knowledge").mkdir()
    (repo_tmp / "events").mkdir()

    store = MAXLegacyStore(root=repo_tmp)

    e = {"type": "promotion", "payload": {"note": "promote"}}
    e_id = store.save_event(e)
    assert e_id.startswith("EV-")

    loaded = store.load_event(e_id)
    assert loaded["id"] == e_id
    assert loaded["type"] == "promotion"

    listed = store.list_events()
    assert e_id in listed
