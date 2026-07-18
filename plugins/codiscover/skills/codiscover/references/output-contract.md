# CoDiscover Output Contract v0.1

Use this compact human-readable structure by default. Omit an empty subsection only when its absence cannot hide a material risk or uncertainty.

## 1. Context Snapshot

- Challenge
- Desired outcome
- Work-system boundary
- Affected people and decisions
- Facts
- Assumptions
- Unknowns
- Confidence

## 2. Candidate Use Cases

For each candidate show:

- title and one-sentence workflow change;
- human role and AI role;
- value profile: Productivity, Impact, Inclusion, Innovation;
- key trade-off;
- principal risk or evidence gap;
- non-AI alternative;
- readiness: Explore, Test, or Hold.

Quick Find returns no more than three. Quick Compare may contain two to five. Quick Sharpen may contain one.

## 3. Recommendation

- Recommended candidate or Hold
- Why now
- Why not the other option first
- Most important uncertainty
- Next safe action

## 4. Minimum Testable Use Case

- Hypothesis
- Scope and sample
- Human owner
- Human checkpoints
- Data boundary
- Baseline
- Success signals
- Failure signals
- Go criteria
- Revise criteria
- Stop criteria
- Review point

## 5. Responsibility Check

State any material issue involving privacy, rights, bias, access, autonomy, appeal, reversibility, resource burden, or missing stakeholder voice.

## 6. Provenance

Summarize:

- User-confirmed
- AI-inferred
- Unknown

## 7. Next Decision

End with one decision or one material question. Do not end with a generic invitation to continue.

## JSON output

When JSON is requested, use `quick-discover-output.schema.json`. Keep explanatory Markdown outside the JSON block so the JSON remains parseable.
