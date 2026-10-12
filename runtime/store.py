from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class MAXLegacyStore:
    """Simple filesystem-backed store for knowledge objects and events.

    - knowledge objects are stored under <repo_root>/knowledge as JSON files named <id>.json
    - events are stored under <repo_root>/events as JSON files named <id>.json

    If an object without an `id` is saved, the store will allocate a new one using
    K-<NNN> for knowledge and EV-<NNNN> for events (event IDs are normally generated
    by EventEngine, but the store can also create them).
    """

    def __init__(self, root: Optional[Path] = None) -> None:
        # Determine repository root relative to this file if not provided
        if root is None:
            root = Path(__file__).resolve().parents[1]
        self.root = root
        self.knowledge_dir = self.root / "knowledge"
        self.events_dir = self.root / "events"
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)

    # ---- knowledge API ----
    def _next_knowledge_id(self) -> str:
        existing = [p.stem for p in self.knowledge_dir.glob("*.json") if p.is_file()]
        nums = []
        for name in existing:
            if name.startswith("K-"):
                try:
                    nums.append(int(name.split("-", 1)[1]))
                except Exception:
                    continue
        next_num = (max(nums) + 1) if nums else 1
        return f"K-{next_num:03d}"

    def save_knowledge(self, obj: Dict[str, Any]) -> str:
        obj = dict(obj)
        obj_id = obj.get("id") or self._next_knowledge_id()
        obj["id"] = obj_id
        path = self.knowledge_dir / f"{obj_id}.json"
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        return obj_id

    def load_knowledge(self, obj_id: str) -> Dict[str, Any]:
        path = self.knowledge_dir / f"{obj_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Knowledge object {obj_id} not found")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_knowledge(self) -> List[str]:
        return sorted([p.stem for p in self.knowledge_dir.glob("*.json") if p.is_file()])

    # Convenience domain-specific save functions
    def save_claim(self, claim: Dict[str, Any]) -> str:
        claim = dict(claim)
        claim.setdefault("type", "claim")
        return self.save_knowledge(claim)

    def save_prediction(self, prediction: Dict[str, Any]) -> str:
        prediction = dict(prediction)
        prediction.setdefault("type", "prediction")
        return self.save_knowledge(prediction)

    def save_experiment(self, experiment: Dict[str, Any]) -> str:
        experiment = dict(experiment)
        experiment.setdefault("type", "experiment")
        return self.save_knowledge(experiment)

    def save_evidence(self, evidence: Dict[str, Any]) -> str:
        evidence = dict(evidence)
        evidence.setdefault("type", "evidence")
        return self.save_knowledge(evidence)

    def save_replication(self, replication: Dict[str, Any]) -> str:
        replication = dict(replication)
        replication.setdefault("type", "replication")
        return self.save_knowledge(replication)

    # ---- events API ----
    def _next_event_id(self) -> str:
        existing = [p.stem for p in self.events_dir.glob("*.json") if p.is_file()]
        nums = []
        for name in existing:
            if name.startswith("EV-"):
                try:
                    nums.append(int(name.split("-", 1)[1]))
                except Exception:
                    continue
        next_num = (max(nums) + 1) if nums else 1
        return f"EV-{next_num:04d}"

    def save_event(self, event: Dict[str, Any]) -> str:
        event = dict(event)
        event_id = event.get("id") or self._next_event_id()
        event["id"] = event_id
        path = self.events_dir / f"{event_id}.json"
        path.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")
        return event_id

    def load_event(self, event_id: str) -> Dict[str, Any]:
        path = self.events_dir / f"{event_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Event {event_id} not found")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_events(self) -> List[str]:
        return sorted([p.stem for p in self.events_dir.glob("*.json") if p.is_file()])
