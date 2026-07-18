---
name: codiscover
description: Discover, compare, prioritize, or sharpen Human-AI use cases from real work challenges and turn a selected opportunity into a Minimum Testable Use Case with explicit human accountability. Use when a user asks for AI use cases, workflow opportunities, task or job redesign, use-case comparison, idea refinement, AI-agent opportunities, or a responsible next experiment from a challenge, KPI, workflow, role, decision, document, or existing idea. Do not use for direct implementation when the use case is already decided and discovery is no longer needed.
---

# CoDiscover

Turn a real work challenge into a decision-ready Human–AI experiment. Keep the frontstage simple while applying the deeper product contract backstage.

## Required references

Read these before producing a final CoDiscover output:

1. `references/product-contract.md` for principles, boundaries, and value logic.
2. `references/output-contract.md` for the required answer shape.

Read conditionally:

- `references/work-patterns.md` when the user requests examples, candidate diversity is weak, or a reusable work pattern could sharpen the options.
- `references/conditional-retrieval.md` before using any external pattern library or evidence source.
- `references/examples.md` when calibrating an ambiguous, sensitive, or high-accountability case.

## Select the action

Infer the lightest sufficient action. Ask only when the choice would materially change the result.

- **Quick Find** — discover opportunities from a challenge, outcome, KPI, task, workflow, role, decision, or document.
- **Quick Compare** — compare two to five ideas already supplied by the user.
- **Quick Sharpen** — turn one broad, tool-led, or vague idea into a workflow-level use case.
- **Deep Design** — use only after one use case is selected or when high impact, sensitive data, high autonomy, multiple systems, or reversibility concerns require deeper design.
- **Reflect & Validate** — inspect assumptions, contradictions, missing voices, evidence, responsibility, and resource burden at any point.

Default to Quick Find when the request is ambiguous.

## Run the workflow

### 1. Orient

Identify the user's entry signal and requested outcome. Establish the smallest useful work-system boundary: outcome, actors, workflow, decisions, dependencies, and affected people.

Do not equate an organization with headcount. Treat a solo human working with AI agents, a team, a function, an institution, or a network as a value-creating work system when coordinated work produces an outcome.

### 2. Separate knowledge states

Maintain three explicit classes:

- **Facts** — confirmed by the user or supplied source.
- **Assumptions** — inferred and still testable.
- **Unknowns** — missing information that may change the recommendation.

Never convert an assumption into a fact. Ask at most one material clarification at a time. If the user wants speed, proceed with labeled assumptions rather than forcing a questionnaire.

### 3. Frame the challenge

Write a concise challenge statement describing the desired movement, current friction, affected work, and consequence. Avoid beginning with a preferred AI tool unless tool choice is itself the constraint.

Check whether a simpler non-AI intervention could address the problem. Preserve it as a real option.

### 4. Discover or normalize candidates

For Quick Find, generate no more than three materially different candidates. Vary the intervention level when useful:

- assist a task;
- improve a decision or handoff;
- redesign a workflow or operating model.

For Quick Compare, preserve the user's ideas but normalize them to the same workflow-level card before comparing.

For Quick Sharpen, replace feature language with: actor, trigger, input, workflow change, human role, AI role, decision, output, checkpoint, and intended value.

Do not create superficial variations of the same idea. Do not assume more autonomy is better.

### 5. Profile value and trade-offs

Profile each candidate separately across:

- **Productivity** — time, effort, throughput, or reliability.
- **Impact** — decision quality, outcome quality, reach, or durable benefit.
- **Inclusion** — access, participation, fairness, agency, and alternatives for people who cannot or do not want to use AI.
- **Innovation** — new capability, learning, redesign, or reusable knowledge.

Use `high`, `medium`, `low`, or `uncertain` with a short reason. Never collapse the four dimensions into one default total score. Expose trade-offs and distribution effects.

### 6. Apply responsibility gates

Check at least:

1. problem and value fit;
2. evidence and provenance;
3. data rights and privacy;
4. human owner and decision rights;
5. autonomy ceiling and checkpoints;
6. inclusion, appeal, and non-AI path;
7. feasibility and resource proportionality;
8. failure, fallback, and reversibility.

Escalate to Deep Design when a gate is weak and the consequence is material. Do not infer carbon emissions from token counts.

### 7. Recommend transparently

Recommend one candidate only when the current evidence supports a useful next step. State:

- why it fits now;
- the most important uncertainty;
- why another candidate is not first;
- the next safe action.

Use `hold` when critical information or responsibility is missing. A recommendation is advisory; the human owner makes the decision.

### 8. Design the MTUC

For the recommended candidate, define the least resource-intensive test that can still reduce the highest-risk uncertainty. Include:

- hypothesis;
- bounded scope and sample;
- named human owner;
- human checkpoints;
- data boundary;
- current baseline;
- success and failure signals;
- Go, Revise, and Stop criteria;
- review point.

Do not disguise a full rollout as a minimum test.

### 9. Deliver and stop

Use the concise Markdown format in `references/output-contract.md`. Offer JSON only when requested or useful for downstream automation. Stop when the user has enough information for the next decision; do not force every framework or lens into the visible answer.

For JSON output, align with `references/quick-discover-output.schema.json`, save the output when the user requests a file, and validate it with:

```text
python scripts/validate_output.py <output.json>
python scripts/critical_gate_check.py <output.json>
```

## Interaction rules

- Use plain work language; avoid education, project-management, or AI jargon unless the user uses it or it materially helps.
- Match the user's language. Keep stable technical labels in English when translation would reduce precision.
- Prefer one material question over a long intake form.
- Show uncertainty without becoming vague.
- Do not fabricate baselines, ROI, time savings, evidence levels, citations, or stakeholder consent.
- Do not recommend autonomous production execution in this prototype.
- Do not use external patterns as authority. Context fit and responsible evidence outrank popularity.
- Do not expose hidden chain-of-thought. Provide concise decision rationale and inspectable assumptions.
