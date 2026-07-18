#!/usr/bin/env python3
"""Repository-level QA for the clean CoDiscover plugin package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codiscover"
SKILL = PLUGIN / "skills" / "codiscover"
VALIDATOR = SKILL / "scripts" / "validate_output.py"
GATES = SKILL / "scripts" / "critical_gate_check.py"
GOLDEN = ROOT / "examples" / "meeting-to-action-output.json"
INVALID = ROOT / "tests" / "fixtures" / "invalid-missing-accountability.json"


def check(condition: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS' if condition else 'FAIL'} | {message}")
    if not condition:
        failures.append(message)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)


def main() -> int:
    failures: list[str] = []

    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    skill_path = SKILL / "SKILL.md"
    required_files = [
        manifest_path,
        marketplace_path,
        skill_path,
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "product-contract.md",
        SKILL / "references" / "output-contract.md",
        SKILL / "references" / "quick-discover-output.schema.json",
        VALIDATOR,
        GATES,
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "SECURITY.md",
        ROOT / "docs" / "judge-testing.md",
        GOLDEN,
        INVALID,
    ]
    for path in required_files:
        check(path.is_file(), f"required file exists: {path.relative_to(ROOT)}", failures)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL | JSON manifest load: {exc}")
        return 1

    check(manifest.get("name") == "codiscover", "plugin name is stable and normalized", failures)
    check(manifest.get("skills") == "./skills/", "plugin points to bundled skills", failures)
    check(manifest.get("author", {}).get("name") == "Chanon Pajunda", "founder attribution is present", failures)
    check(manifest.get("license") == "MIT", "manifest and repository license agree", failures)
    entries = marketplace.get("plugins", [])
    matching = [entry for entry in entries if entry.get("name") == "codiscover"]
    check(len(matching) == 1, "marketplace contains one CoDiscover entry", failures)
    if matching:
        entry = matching[0]
        check(entry.get("source", {}).get("path") == "./plugins/codiscover", "marketplace source path is repo-relative", failures)
        check(entry.get("policy", {}).get("installation") == "AVAILABLE", "plugin is available for install", failures)

    forbidden_markers = ["[TODO:", "course-evidence/", "raw-evidence/", "private/"]
    text_files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".txt"}]
    for marker in forbidden_markers[:1]:
        hits = [str(path.relative_to(ROOT)) for path in text_files if marker in path.read_text(encoding="utf-8", errors="ignore")]
        check(not hits, f"no scaffold placeholder {marker}", failures)

    forbidden_extensions = {".docx", ".pdf", ".xlsx", ".pptx"}
    restricted_files = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in forbidden_extensions]
    check(not restricted_files, "no binary internal-document formats are included", failures)

    golden_validation = run([sys.executable, str(VALIDATOR), str(GOLDEN)])
    check(golden_validation.returncode == 0, "golden example passes structural validation", failures)
    if golden_validation.returncode != 0:
        print(golden_validation.stdout)
        print(golden_validation.stderr)

    golden_gates = run([sys.executable, str(GATES), str(GOLDEN)])
    check(golden_gates.returncode == 0, "golden example passes critical gates", failures)
    if golden_gates.returncode != 0:
        print(golden_gates.stdout)
        print(golden_gates.stderr)

    invalid_validation = run([sys.executable, str(VALIDATOR), str(INVALID)])
    check(invalid_validation.returncode != 0, "invalid example is rejected", failures)

    if failures:
        print(f"\nQA RESULT: FAIL ({len(failures)} checks failed)")
        return 1
    print("\nQA RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
