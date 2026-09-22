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
SCHEMA_VERSIONS = {"0.1", "0.2"}
REDESIGN_ROUTE_IDS = {"enhance", "redesign", "reimagine"}
DECISION_GATE_TYPES = {"road", "junction", "checkpoint", "sensor", "u_turn", "exit"}
META_LAB_LABELS = {"observation", "hypothesis", "emerging_pattern", "principle_candidate"}


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

    if data.get("schema_version") not in SCHEMA_VERSIONS:
        errors.append("$.schema_version: expected '0.1' or '0.2'")
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
    if "redesign" in data:
        validate_redesign(data.get("redesign"), errors)
    if "meta_lab" in data:
        validate_meta_lab(data.get("meta_lab"), errors)
    return errors


def validate_redesign(raw: Any, errors: list[str]) -> None:
    path = "$.redesign"
    redesign = require_object(raw, path, errors)
    require_keys(
        redesign,
        {"status", "redesign_unit", "as_is_xray", "lean_scan", "routes", "decision_gates", "recommended_route"},
        path,
        errors,
    )
    if redesign.get("status") not in {"not_started", "ready", "hold"}:
        errors.append(f"{path}.status: expected not_started, ready, or hold")
    require_text(redesign.get("redesign_unit"), f"{path}.redesign_unit", errors)

    as_is = require_object(redesign.get("as_is_xray"), f"{path}.as_is_xray", errors)
    as_is_keys = {"current_work", "waste", "necessary_work", "decisions", "evidence", "constraints", "unknowns"}
    require_keys(as_is, as_is_keys, f"{path}.as_is_xray", errors)
    for field in sorted(as_is_keys):
        require_list(as_is.get(field), f"{path}.as_is_xray.{field}", errors)

    lean = require_object(redesign.get("lean_scan"), f"{path}.lean_scan", errors)
    lean_keys = {"waste", "necessary_work", "decision_points", "capability_add"}
    require_keys(lean, lean_keys, f"{path}.lean_scan", errors)
    for field in sorted(lean_keys):
        require_list(lean.get(field), f"{path}.lean_scan.{field}", errors)

    routes = require_list(redesign.get("routes"), f"{path}.routes", errors, nonempty=True)
    if len(routes) < 2 or len(routes) > 3:
        errors.append(f"{path}.routes: expected 2 to 3 routes")
    route_ids: set[str] = set()
    route_keys = {
        "id", "summary", "workflow_change", "efficiency_gain", "new_capability",
        "human_role", "ai_role", "risks", "evidence_needed", "minimum_experiment",
    }
    for index, raw_route in enumerate(routes):
        route_path = f"{path}.routes[{index}]"
        route = require_object(raw_route, route_path, errors)
        require_keys(route, route_keys, route_path, errors)
        route_id = route.get("id")
        if route_id not in REDESIGN_ROUTE_IDS:
            errors.append(f"{route_path}.id: expected one of {sorted(REDESIGN_ROUTE_IDS)}")
        if route_id in route_ids:
            errors.append(f"{route_path}.id: duplicate route id {route_id}")
        route_ids.add(route_id)
        for field in ("summary", "workflow_change", "efficiency_gain", "new_capability", "human_role", "ai_role", "minimum_experiment"):
            require_text(route.get(field), f"{route_path}.{field}", errors)
        for field in ("risks", "evidence_needed"):
            require_list(route.get(field), f"{route_path}.{field}", errors, nonempty=True)

    gates = require_list(redesign.get("decision_gates"), f"{path}.decision_gates", errors, nonempty=True)
    gate_keys = {"id", "type", "state", "evidence", "success_conditions", "constraints", "options", "decision_owner", "human_checkpoint", "next_action", "u_turn_condition", "exit_condition"}
    for index, raw_gate in enumerate(gates):
        gate_path = f"{path}.decision_gates[{index}]"
        gate = require_object(raw_gate, gate_path, errors)
        require_keys(gate, gate_keys, gate_path, errors)
        require_text(gate.get("id"), f"{gate_path}.id", errors)
        if gate.get("type") not in DECISION_GATE_TYPES:
            errors.append(f"{gate_path}.type: invalid decision gate type")
        for field in ("state", "decision_owner", "human_checkpoint", "next_action", "u_turn_condition", "exit_condition"):
            require_text(gate.get(field), f"{gate_path}.{field}", errors)
        for field in ("evidence", "success_conditions", "constraints", "options"):
            require_list(gate.get(field), f"{gate_path}.{field}", errors)
    if redesign.get("recommended_route") not in REDESIGN_ROUTE_IDS | {"hold"}:
        errors.append(f"{path}.recommended_route: expected route id or hold")
    if redesign.get("recommended_route") in REDESIGN_ROUTE_IDS and redesign.get("recommended_route") not in route_ids:
        errors.append(f"{path}.recommended_route: must reference one of routes")


def validate_meta_lab(raw: Any, errors: list[str]) -> None:
    path = "$.meta_lab"
    meta = require_object(raw, path, errors)
    keys = {"status", "case_ids", "repeat", "difference", "surprise", "missing", "reusable", "evidence_ladder", "delivery_asset", "learning_asset"}
    require_keys(meta, keys, path, errors)
    if meta.get("status") not in {"not_started", "draft", "candidate"}:
        errors.append(f"{path}.status: expected not_started, draft, or candidate")
    case_ids = require_list(meta.get("case_ids"), f"{path}.case_ids", errors, nonempty=True)
    if len(case_ids) < 2:
        errors.append(f"{path}.case_ids: requires at least two cases")
    for index, case_id in enumerate(case_ids):
        require_text(case_id, f"{path}.case_ids[{index}]", errors)
    for field in ("repeat", "difference", "surprise", "missing", "reusable"):
        require_list(meta.get(field), f"{path}.{field}", errors)
    ladder = require_list(meta.get("evidence_ladder"), f"{path}.evidence_ladder", errors, nonempty=True)
    ladder_keys = {"label", "statement", "supporting_cases"}
    for index, raw_item in enumerate(ladder):
        item_path = f"{path}.evidence_ladder[{index}]"
        item = require_object(raw_item, item_path, errors)
        require_keys(item, ladder_keys, item_path, errors)
        if item.get("label") not in META_LAB_LABELS:
            errors.append(f"{item_path}.label: invalid evidence ladder label")
        require_text(item.get("statement"), f"{item_path}.statement", errors)
        supporting = require_list(item.get("supporting_cases"), f"{item_path}.supporting_cases", errors, nonempty=True)
        for case_index, case_id in enumerate(supporting):
            require_text(case_id, f"{item_path}.supporting_cases[{case_index}]", errors)
    require_text(meta.get("delivery_asset"), f"{path}.delivery_asset", errors)
    require_text(meta.get("learning_asset"), f"{path}.learning_asset", errors)


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
    print(f"VALID: CoDiscover output contract v{document.get('schema_version')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
