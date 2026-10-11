#!/usr/bin/env python3
"""
MAX-LEGACY Knowledge Validator v0.1
Enforces knowledge lifecycle and promotion rules.
"""

import json
import sys
from typing import Dict, Tuple

KNOWLEDGE_STATES = [
    "claim",
    "prediction",
    "experiment",
    "evidence",
    "replication",
    "knowledge"
]

STATE_TRANSITIONS = {
    "claim": ["prediction"],
    "prediction": ["experiment"],
    "experiment": ["evidence"],
    "evidence": ["replication"],
    "replication": ["knowledge"],
    "knowledge": []
}

PROMOTION_RULES = {
    "claim_to_prediction": {"min_confidence": 0, "min_alignment": 0},
    "prediction_to_experiment": {"min_confidence": 20, "min_alignment": 10},
    "experiment_to_evidence": {"min_confidence": 40, "min_alignment": 30},
    "evidence_to_replication": {"min_confidence": 55, "min_alignment": 50},
    "replication_to_knowledge": {"min_confidence": 75, "min_alignment": 70, "final_status": "Validated"}
}

def validate_confidence_range(confidence: float) -> Tuple[bool, str]:
    """Validate confidence is in range [0, 100]."""
    if not isinstance(confidence, (int, float)):
        return False, f"Confidence must be a number, got {type(confidence)}"
    if confidence < 0 or confidence > 100:
        return False, f"Confidence {confidence} out of range [0, 100]"
    return True, "Confidence range valid"

def validate_reality_alignment(alignment: float) -> Tuple[bool, str]:
    """Validate reality alignment is in range [0, 100]."""
    if not isinstance(alignment, (int, float)):
        return False, f"Reality alignment must be a number, got {type(alignment)}"
    if alignment < 0 or alignment > 100:
        return False, f"Reality alignment {alignment} out of range [0, 100]"
    return True, "Reality alignment range valid"

def validate_state_transition(from_state: str, to_state: str) -> Tuple[bool, str]:
    """Validate state transition is allowed."""
    if from_state not in STATE_TRANSITIONS:
        return False, f"Unknown state: {from_state}"
    if to_state not in STATE_TRANSITIONS[from_state]:
        return False, f"Invalid transition: {from_state} → {to_state}"
    return True, f"Valid transition: {from_state} → {to_state}"

def validate_knowledge_object(knowledge: Dict) -> Tuple[bool, str, Dict]:
    """Validate complete knowledge object."""
    report = {
        "checks": {},
        "status": "FAIL",
        "errors": []
    }

    required_fields = [
        "knowledge_id", "claim_id", "prediction_id", "experiment_id",
        "evidence_id", "replication_id", "confidence", "reality_alignment", "status"
    ]

    for field in required_fields:
        if field not in knowledge:
            report["errors"].append(f"Missing required field: {field}")

    if report["errors"]:
        return False, "Missing required fields", report

    conf_valid, conf_msg = validate_confidence_range(knowledge["confidence"])
    report["checks"]["confidence_range"] = {"passed": conf_valid, "message": conf_msg}
    if not conf_valid:
        report["errors"].append(conf_msg)

    align_valid, align_msg = validate_reality_alignment(knowledge["reality_alignment"])
    report["checks"]["reality_alignment_range"] = {"passed": align_valid, "message": align_msg}
    if not align_valid:
        report["errors"].append(align_msg)

    if knowledge["status"] not in KNOWLEDGE_STATES:
        report["errors"].append(f"Invalid status: {knowledge['status']}")
    else:
        report["checks"]["status_valid"] = {"passed": True, "message": f"Status '{knowledge['status']}' is valid"}

    if "lifecycle_history" in knowledge:
        lifecycle_valid = True
        lifecycle_errors = []

        prev_state = None
        for event in knowledge["lifecycle_history"]:
            state = event.get("state")
            conf = event.get("confidence")
            align = event.get("reality_alignment")

            if prev_state:
                trans_valid, trans_msg = validate_state_transition(prev_state, state)
                if not trans_valid:
                    lifecycle_valid = False
                    lifecycle_errors.append(trans_msg)

            conf_valid, _ = validate_confidence_range(conf)
            align_valid, _ = validate_reality_alignment(align)

            if not conf_valid or not align_valid:
                lifecycle_valid = False
                lifecycle_errors.append(f"Invalid metrics at state '{state}'")

            prev_state = state

        report["checks"]["lifecycle_history"] = {
            "passed": lifecycle_valid,
            "message": "Lifecycle history valid" if lifecycle_valid else "; ".join(lifecycle_errors)
        }
        if not lifecycle_valid:
            report["errors"].extend(lifecycle_errors)

    if not report["errors"]:
        report["status"] = "PASS"
        return True, "Knowledge object validation passed", report

    return False, "Knowledge object validation failed", report

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_knowledge.py <knowledge_object.json>")
        sys.exit(1)

    knowledge_file = sys.argv[1]

    try:
        with open(knowledge_file, "r") as f:
            knowledge = json.load(f)
    except Exception as e:
        print(f"FAIL: Could not load {knowledge_file}: {e}")
        sys.exit(1)

    valid, message, report = validate_knowledge_object(knowledge)

    print(json.dumps(report, indent=2))
    print(f"\n{report['status']}: {message}")

    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
