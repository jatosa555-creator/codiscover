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

## ChatGPT App / mobile layer

```text
ChatGPT web or mobile conversation
  -> Add @CoDiscover
  -> ChatGPT selects a read-only MCP tool
  -> discover_use_cases / compare_use_cases / sharpen_use_case
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
