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

## Core and optional layers

CoDiscover remains one product with three composable layers:

```text
CoDiscover Core
  Discover → Decide → MTUC
        │
        ├─ ReDesign Extension (optional after selection)
        │    As-Is X-ray → Lean scan → Enhance / Redesign / Reimagine
        │    → decision gates → minimum experiment
        │
        └─ Meta-Lab Learning Layer (optional with 2+ completed cases)
             Repeat / Difference / Surprise / Missing / Reusable
             → evidence ladder → delivery asset + learning asset
```

The Core frontstage and v0.1 output contract stay valid. Schema v0.2 adds only optional `redesign` and `meta_lab` sections. ReDesign changes how a selected workflow is designed; Meta-Lab compares completed traces and does not silently change a live workflow. Both layers keep a human decision owner and the advisory boundary.

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
- `references/redesign-extension.md` defines the optional workflow redesign trace.
- `references/meta-lab.md` defines the optional multi-case learning record.

## ChatGPT App / mobile layer

```text
ChatGPT web or mobile conversation
  -> Add @CoDiscover
  -> ChatGPT selects a read-only MCP tool
  -> discover_use_cases / compare_use_cases / sharpen_use_case
  -> redesign_workflow / learn_from_traces (optional layers)
  -> CoDiscover returns structured decision support
  -> ChatGPT explains it in the user's language
  -> A human owner makes the decision
```

- `apps/chatgpt-mcp/server.js` exposes a stateless Streamable HTTP MCP endpoint at `/mcp`.
- `apps/chatgpt-mcp/discovery.js` contains a compact, redistribution-safe pattern engine aligned with the product contract.
- No separate website or Custom GPT is required for the user experience.
- No OpenAI API key is required by the current server; the host conversation handles language and synthesis.
- Public mobile availability requires stable HTTPS hosting, a platform-issued Apps SDK app ID, and OpenAI plugin publication.

## Retrieval architecture

- K1: current user context;
- K2: original bundled CoDiscover work patterns;
- K3: conditional authorized external retrieval.

The v0.1 repository does not bundle third-party course evidence. K3 remains disabled unless an authorized source is supplied or connected.
