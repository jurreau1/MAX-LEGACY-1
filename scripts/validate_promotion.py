#!/usr/bin/env python3
"""
MAX-LEGACY Promotion Validator v0.1
Enforces promotion rules and emits evolution events.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Tuple

PROMOTION_RULES = {
    "claim_to_prediction": {"min_confidence": 0, "min_alignment": 0},
    "prediction_to_experiment": {"min_confidence": 20, "min_alignment": 10},
    "experiment_to_evidence": {"min_confidence": 40, "min_alignment": 30},
    "evidence_to_replication": {"min_confidence": 55, "min_alignment": 50},
    "replication_to_knowledge": {"min_confidence": 75, "min_alignment": 70, "final_status": "Validated"}
}

REALITY_ALIGNMENT_LEVELS = {
    "concept": {"minimum": 0, "maximum": 10},
    "formalized": {"minimum": 10, "maximum": 25},
    "simulated": {"minimum": 25, "maximum": 40},
    "predicted": {"minimum": 40, "maximum": 55},
    "evidence_supported": {"minimum": 55, "maximum": 70},
    "replicated": {"minimum": 70, "maximum": 85},
    "established": {"minimum": 85, "maximum": 95},
    "reality_aligned": {"minimum": 95, "maximum": 100}
}

def get_alignment_level(score: float) -> str:
    """Get the alignment level for a given score."""
    for level, bounds in REALITY_ALIGNMENT_LEVELS.items():
        if bounds["minimum"] <= score <= bounds["maximum"]:
            return level
    return "unknown"

def validate_promotion(from_state: str, to_state: str, confidence: float, alignment: float) -> Tuple[bool, str, Dict]:
    """Validate promotion against promotion rules."""
    transition_key = f"{from_state}_to_{to_state}"

    if transition_key not in PROMOTION_RULES:
        return False, f"Unknown promotion rule: {transition_key}", {}

    rule = PROMOTION_RULES[transition_key]
    min_confidence = rule["min_confidence"]
    min_alignment = rule["min_alignment"]

    validation_details = {
        "rule": transition_key,
        "min_confidence_required": min_confidence,
        "min_alignment_required": min_alignment,
        "confidence_actual": confidence,
        "alignment_actual": alignment,
        "confidence_check": {
            "required": min_confidence,
            "actual": confidence,
            "passed": confidence >= min_confidence
        },
        "alignment_check": {
            "required": min_alignment,
            "actual": alignment,
            "passed": alignment >= min_alignment
        },
        "alignment_level": get_alignment_level(alignment),
        "state_transition_check": {
            "from": from_state,
            "to": to_state,
            "valid": True
        }
    }

    if confidence < min_confidence:
        validation_details["confidence_check"]["passed"] = False
        return False, f"Confidence {confidence} below minimum {min_confidence}", validation_details

    if alignment < min_alignment:
        validation_details["alignment_check"]["passed"] = False
        return False, f"Alignment {alignment} below minimum {min_alignment}", validation_details

    if "final_status" in rule:
        validation_details["final_status"] = rule["final_status"]

    message = f"Promotion valid: {transition_key}"
    return True, message, validation_details

def get_next_event_id(output_dir: str = "events") -> str:
    """Get the next event ID."""
    if not os.path.exists(output_dir):
        return "EV-0002"
    
    files = [f for f in os.listdir(output_dir) if f.startswith("EV-") and f.endswith(".json")]
    if not files:
        return "EV-0002"
    
    max_num = max([int(f[3:-5]) for f in files])
    return f"EV-{max_num + 1:04d}"

def create_evolution_event(knowledge_id: str, domain: str, from_state: str, to_state: str,
                          confidence_before: float, confidence_after: float,
                          alignment_before: float, alignment_after: float,
                          validation_details: Dict) -> Dict:
    """Create an evolution event for promotion."""
    event_id = get_next_event_id()

    event = {
        "event_id": event_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "domain": domain,
        "entity_id": knowledge_id,
        "change_type": f"{to_state}_promoted",
        "actor": "promotion_validator",
        "from_state": from_state,
        "to_state": to_state,
        "confidence_before": confidence_before,
        "confidence_after": confidence_after,
        "reality_alignment_before": alignment_before,
        "reality_alignment_after": alignment_after,
        "validation_passed": True,
        "validation_details": validation_details,
        "description": f"Knowledge object {knowledge_id} promoted from {from_state} to {to_state}"
    }

    return event

def save_evolution_event(event: Dict, output_dir: str = "events") -> bool:
    """Save evolution event to file."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        event_file = os.path.join(output_dir, f"{event['event_id']}.json")
        with open(event_file, "w") as f:
            json.dump(event, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving event: {e}")
        return False

def main():
    if len(sys.argv) < 8:
        print("Usage: validate_promotion.py <knowledge_id> <domain> <from_state> <to_state> <confidence_after> <alignment_after> [--emit-event]")
        print("\nExample: validate_promotion.py K-001 research replication knowledge 85 82 --emit-event")
        sys.exit(1)

    knowledge_id = sys.argv[1]
    domain = sys.argv[2]
    from_state = sys.argv[3]
    to_state = sys.argv[4]
    confidence_after = float(sys.argv[5])
    alignment_after = float(sys.argv[6])
    emit_event = "--emit-event" in sys.argv

    confidence_before = confidence_after - 10 if confidence_after >= 10 else 0
    alignment_before = alignment_after - 10 if alignment_after >= 10 else 0

    valid, message, validation_details = validate_promotion(
        from_state, to_state, confidence_after, alignment_after
    )

    report = {
        "knowledge_id": knowledge_id,
        "domain": domain,
        "promotion": {
            "from_state": from_state,
            "to_state": to_state,
            "valid": valid
        },
        "validation_details": validation_details,
        "message": message,
        "status": "PASS" if valid else "FAIL"
    }

    if valid and emit_event:
        event = create_evolution_event(
            knowledge_id, domain, from_state, to_state,
            confidence_before, confidence_after,
            alignment_before, alignment_after,
            validation_details
        )
        if save_evolution_event(event):
            report["evolution_event"] = event
            report["event_saved"] = True
        else:
            report["event_saved"] = False

    print(json.dumps(report, indent=2))
    print(f"\n{report['status']}: {message}")

    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
