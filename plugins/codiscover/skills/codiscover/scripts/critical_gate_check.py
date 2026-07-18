#!/usr/bin/env python3
"""Run decision-critical checks beyond structural validation."""

from __future__ import annotations

import sys
from pathlib import Path

from validate_output import load_document, validate_document


def gate_results(document: dict) -> list[tuple[str, bool, str]]:
    context = document.get("context_snapshot", {})
    candidates = document.get("candidate_use_cases", [])
    recommendation = document.get("recommendation", {})
    mtuc = document.get("mtuc", {})
    responsibility = document.get("responsibility_check", {})
    provenance = document.get("provenance", {})

    return [
        ("G1 problem-value fit", bool(context.get("challenge") and context.get("desired_outcome")), "Challenge and desired outcome are explicit"),
        ("G2 evidence and provenance", all(key in provenance for key in ("user_confirmed", "ai_inferred", "unknown")), "Knowledge states are separated"),
        ("G3 data rights and privacy", bool(mtuc.get("data_boundary")), "MTUC states its data boundary"),
        ("G4 human accountability", bool(mtuc.get("owner")) and bool(mtuc.get("human_checkpoints")), "Owner and checkpoints are named"),
        ("G5 autonomy ceiling", all(bool(candidate.get("human_role")) and bool(candidate.get("ai_role")) for candidate in candidates), "Human and AI roles are explicit"),
        ("G6 inclusion and non-AI path", all(bool(candidate.get("non_ai_alternative")) and "inclusion" in candidate.get("value_profile", {}) for candidate in candidates), "Inclusion and non-AI alternatives are visible"),
        ("G7 proportional feasibility", all(bool(candidate.get("tradeoffs")) and bool(candidate.get("evidence_gaps")) for candidate in candidates), "Trade-offs and evidence gaps are explicit"),
        ("G8 failure and reversibility", bool(mtuc.get("failure_signals")) and bool(mtuc.get("stop_criteria")), "Failure and stop criteria are testable"),
        ("G9 decision traceability", recommendation.get("decision") in {"recommend", "hold"} and bool(recommendation.get("key_uncertainty")), "Recommendation exposes uncertainty"),
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: critical_gate_check.py <output.json>", file=sys.stderr)
        return 2
    try:
        document = load_document(Path(argv[1]))
    except Exception as exc:  # noqa: BLE001 - CLI must report all load failures cleanly
        print(f"FAIL: cannot load output: {exc}")
        return 1

    structural_errors = validate_document(document)
    if structural_errors:
        print("FAIL: structural validation failed before critical gates")
        for error in structural_errors:
            print(f"- {error}")
        return 1

    results = gate_results(document)
    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'} | {name} | {detail}")
    failed = [name for name, passed, _ in results if not passed]
    if failed:
        print(f"CRITICAL GATE RESULT: FAIL ({len(failed)} failed)")
        return 1
    print("CRITICAL GATE RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
