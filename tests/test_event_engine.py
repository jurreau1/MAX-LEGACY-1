from runtime.store import MAXLegacyStore
from runtime.event_engine import EventEngine


def test_event_increment_and_persistence(tmp_path):
    repo_tmp = tmp_path / "repo"
    repo_tmp.mkdir()
    (repo_tmp / "knowledge").mkdir()
    (repo_tmp / "events").mkdir()

    store = MAXLegacyStore(root=repo_tmp)
    engine = EventEngine(store=store)

    e1 = engine.emit_promotion_event({"step": 1})
    e2 = engine.emit_promotion_event({"step": 2})
    e3 = engine.emit_validation_event({"ok": True})

    assert e1["id"].startswith("EV-")
    assert e2["id"].startswith("EV-")
    assert e3["id"].startswith("EV-")

    # ensure incrementing order
    ids = [e1["id"], e2["id"], e3["id"]]
    assert ids == sorted(ids)

    # create a fresh engine backed by the same store to verify persistence
    engine2 = EventEngine(store=store)
    next_id = engine2.next_event_id()
    # next id should be greater than the last emitted id
    assert next_id > e3["id"]
