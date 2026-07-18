# Architecture

## Frontstage

```text
Add CoDiscover
      ↓
Describe a challenge, ideas, or a broad use case
      ↓
Quick Find / Quick Compare / Quick Sharpen
      ↓
Context Snapshot + Candidate Use Cases
      ↓
Four-Value Profile + Responsibility Gates
      ↓
Recommendation + MTUC + Next Decision
```

## Backstage

```text
Entry signal
  → Work-system framing
  → Knowledge-state separation
  → Candidate discovery or normalization
  → Value and trade-off profiling
  → Human–AI role design
  → Responsibility gates
  → Recommendation
  → Minimum Testable Use Case
  → Structured validation
```

## Plugin package

- `.codex-plugin/plugin.json` supplies install-surface metadata.
- `skills/codiscover/SKILL.md` routes and executes the discovery workflow.
- `references/` provides progressively loaded product and output contracts.
- `scripts/validate_output.py` checks structural conformance.
- `scripts/critical_gate_check.py` checks decision-critical safeguards.

## Retrieval architecture

- K1: current user context;
- K2: original bundled CoDiscover work patterns;
- K3: conditional authorized external retrieval.

The v0.1 repository does not bundle third-party course evidence. K3 remains disabled unless an authorized source is supplied or connected.
