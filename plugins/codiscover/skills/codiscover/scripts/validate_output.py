#!/usr/bin/env python3
"""Validate a CoDiscover JSON output without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


VALUE_LEVELS = {"high", "medium", "low", "uncertain"}
READINESS = {"explore", "test", "hold"}
MODES = {"quick_find", "quick_compare", "quick_sharpen", "deep_design"}


def load_document(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON value must be an object")
    return data


def require_object(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return {}
    return value


def require_list(value: Any, path: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return []
    if nonempty and not value:
        errors.append(f"{path}: must not be empty")
    return value


def require_text(value: Any, path: str, errors: list[str], *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        errors.append(f"{path}: expected string")
        return ""
    if nonempty and not value.strip():
        errors.append(f"{path}: must not be blank")
    return value


def require_keys(obj: dict[str, Any], keys: set[str], path: str, errors: list[str]) -> None:
    for key in sorted(keys - obj.keys()):
        errors.append(f"{path}.{key}: missing required field")


def validate_document(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    top = {
        "schema_version", "mode", "language", "context_snapshot",
        "candidate_use_cases", "recommendation", "mtuc",
        "responsibility_check", "provenance", "next_decision",
    }
    require_keys(data, top, "$", errors)

    if data.get("schema_version") != "0.1":
        errors.append("$.schema_version: expected '0.1'")
    if data.get("mode") not in MODES:
        errors.append(f"$.mode: expected one of {sorted(MODES)}")
    require_text(data.get("language"), "$.language", errors)

    context = require_object(data.get("context_snapshot"), "$.context_snapshot", errors)
    context_keys = {
        "challenge", "desired_outcome", "work_system_boundary", "affected_people",
        "decisions", "facts", "assumptions", "unknowns", "confidence",
    }
    require_keys(context, context_keys, "$.context_snapshot", errors)
    for field in ("challenge", "desired_outcome", "work_system_boundary"):
        require_text(context.get(field), f"$.context_snapshot.{field}", errors)
    for field in ("affected_people", "decisions", "facts", "assumptions", "unknowns"):
        require_list(context.get(field), f"$.context_snapshot.{field}", errors)
    if context.get("confidence") not in {"high", "medium", "low"}:
        errors.append("$.context_snapshot.confidence: expected high, medium, or low")

    candidates = require_list(data.get("candidate_use_cases"), "$.candidate_use_cases", errors, nonempty=True)
    if len(candidates) > 5:
        errors.append("$.candidate_use_cases: maximum is 5")
    if data.get("mode") == "quick_find" and len(candidates) > 3:
        errors.append("$.candidate_use_cases: Quick Find maximum is 3")

    seen_ids: set[str] = set()
    candidate_keys = {
        "id", "title", "workflow_change", "human_role", "ai_role", "value_profile",
        "tradeoffs", "risks", "evidence_gaps", "non_ai_alternative", "readiness",
    }
    for index, raw_candidate in enumerate(candidates):
        path = f"$.candidate_use_cases[{index}]"
        candidate = require_object(raw_candidate, path, errors)
        require_keys(candidate, candidate_keys, path, errors)
        candidate_id = require_text(candidate.get("id"), f"{path}.id", errors)
        if candidate_id and not re.fullmatch(r"UC-[0-9]{2}", candidate_id):
            errors.append(f"{path}.id: expected format UC-01")
        if candidate_id in seen_ids:
            errors.append(f"{path}.id: duplicate id {candidate_id}")
        seen_ids.add(candidate_id)
        for field in ("title", "workflow_change", "human_role", "ai_role", "non_ai_alternative"):
            require_text(candidate.get(field), f"{path}.{field}", errors)
        for field in ("tradeoffs", "risks", "evidence_gaps"):
            require_list(candidate.get(field), f"{path}.{field}", errors, nonempty=True)
        if candidate.get("readiness") not in READINESS:
            errors.append(f"{path}.readiness: expected one of {sorted(READINESS)}")
        profile = require_object(candidate.get("value_profile"), f"{path}.value_profile", errors)
        for dimension in ("productivity", "impact", "inclusion", "innovation"):
            value = require_object(profile.get(dimension), f"{path}.value_profile.{dimension}", errors)
            if value.get("level") not in VALUE_LEVELS:
                errors.append(f"{path}.value_profile.{dimension}.level: invalid value")
            require_text(value.get("reason"), f"{path}.value_profile.{dimension}.reason", errors)

    recommendation = require_object(data.get("recommendation"), "$.recommendation", errors)
    recommendation_keys = {"decision", "use_case_id", "why_now", "why_not_others_first", "key_uncertainty", "next_safe_action"}
    require_keys(recommendation, recommendation_keys, "$.recommendation", errors)
    if recommendation.get("decision") not in {"recommend", "hold"}:
        errors.append("$.recommendation.decision: expected recommend or hold")
    recommended_id = recommendation.get("use_case_id")
    if recommendation.get("decision") == "recommend" and recommended_id not in seen_ids:
        errors.append("$.recommendation.use_case_id: must reference a candidate")
    if recommendation.get("decision") == "hold" and recommended_id is not None:
        errors.append("$.recommendation.use_case_id: must be null when decision is hold")
    for field in ("why_now", "why_not_others_first", "key_uncertainty", "next_safe_action"):
        require_text(recommendation.get(field), f"$.recommendation.{field}", errors, nonempty=field in {"key_uncertainty", "next_safe_action"})

    mtuc = require_object(data.get("mtuc"), "$.mtuc", errors)
    mtuc_keys = {
        "status", "hypothesis", "scope", "owner", "human_checkpoints", "data_boundary",
        "baseline", "success_signals", "failure_signals", "go_criteria", "revise_criteria",
        "stop_criteria", "review_point",
    }
    require_keys(mtuc, mtuc_keys, "$.mtuc", errors)
    if mtuc.get("status") not in {"ready", "provisional", "not_ready"}:
        errors.append("$.mtuc.status: expected ready, provisional, or not_ready")
    for field in ("hypothesis", "scope", "owner", "data_boundary", "baseline", "review_point"):
        require_text(mtuc.get(field), f"$.mtuc.{field}", errors, nonempty=mtuc.get("status") != "not_ready")
    for field in ("human_checkpoints", "success_signals", "failure_signals", "go_criteria", "revise_criteria", "stop_criteria"):
        require_list(mtuc.get(field), f"$.mtuc.{field}", errors, nonempty=mtuc.get("status") == "ready")

    responsibility = require_object(data.get("responsibility_check"), "$.responsibility_check", errors)
    require_keys(responsibility, {"status", "issues", "required_controls"}, "$.responsibility_check", errors)
    if responsibility.get("status") not in {"pass", "revise", "stop"}:
        errors.append("$.responsibility_check.status: expected pass, revise, or stop")
    require_list(responsibility.get("issues"), "$.responsibility_check.issues", errors)
    require_list(responsibility.get("required_controls"), "$.responsibility_check.required_controls", errors)

    provenance = require_object(data.get("provenance"), "$.provenance", errors)
    require_keys(provenance, {"user_confirmed", "ai_inferred", "unknown"}, "$.provenance", errors)
    for field in ("user_confirmed", "ai_inferred", "unknown"):
        require_list(provenance.get(field), f"$.provenance.{field}", errors)

    require_text(data.get("next_decision"), "$.next_decision", errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_output.py <output.json>", file=sys.stderr)
        return 2
    try:
        document = load_document(argv[1])
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}")
        return 1
    errors = validate_document(document)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: CoDiscover output contract v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
