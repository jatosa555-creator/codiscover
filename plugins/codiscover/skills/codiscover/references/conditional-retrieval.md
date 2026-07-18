# Conditional Pattern Retrieval Policy

## Retrieval layers

- **K1 — Current context:** user-provided challenge, files, statements, constraints, and decisions.
- **K2 — Internal product patterns:** original CoDiscover work-pattern abstractions bundled with this skill.
- **K3 — External patterns:** authorized external libraries, connected sources, or evidence supplied by the user.

## Default behavior

Use K1 first and K2 only when it improves candidate diversity or workflow precision. K3 is conditional and disabled when no authorized source is available.

Retrieve K3 only when at least one condition is true:

- the user explicitly asks for examples or external comparison;
- current candidates are generic or repetitive;
- domain specificity materially changes risk or feasibility;
- the user supplies or authorizes a source;
- evidence is needed for a claim that should not rest on model memory.

## Guardrails

- Never imply that an external source was searched when no retrieval occurred.
- Record source, confidence, evidence level, and transfer rationale.
- Treat examples as patterns, not proof that a use case will work in the user's context.
- Do not copy paid-course wording, proprietary checklists, confidential cases, or unlicensed material.
- Popularity cannot override context fit, human accountability, or critical gates.
- If K3 does not materially change the decision, say so and prefer the lower-cost K1/K2 result.

## Retrieval stop rule

Stop when additional patterns no longer change candidate diversity, risk understanding, or the next test. Do not retrieve merely to make the answer appear researched.
