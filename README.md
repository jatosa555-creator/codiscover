# CoDiscover

**From a real work challenge to a decision-ready Human–AI experiment.**

CoDiscover is a skill-first plugin for ChatGPT and Codex. It helps a person working alone, with a team, or across an organization discover, compare, and sharpen AI use cases without reducing value to time savings alone.

CoDiscover profiles four forms of value:

- Productivity
- Impact
- Inclusion
- Innovation

It then turns the recommended opportunity into a **Minimum Testable Use Case (MTUC)** with a named human owner, evidence signals, checkpoints, and Go/Revise/Stop criteria.

## What makes it different

Most AI use-case generators stop at an idea list. CoDiscover connects five decisions:

1. What is the real work challenge?
2. Where could intervention create value?
3. How should humans and AI share the work?
4. What is the smallest responsible test?
5. What evidence should lead to Go, Revise, or Stop?

## Quick start

### Install from this repository marketplace

This repository includes a local marketplace at `.agents/plugins/marketplace.json` and the plugin at `plugins/codiscover`.

1. Clone the public repository:

   ```text
   git clone https://github.com/jatosa555-creator/codiscover.git
   cd codiscover
   ```

2. Add the repository marketplace to Codex:

   ```text
   codex plugin marketplace add <absolute-path-to-this-repository>
   ```

3. Install the plugin:

   ```text
   codex plugin add codiscover@personal
   ```

4. Restart the ChatGPT desktop app or start a new Codex task.

5. Invoke the skill explicitly:

   ```text
   Use $codiscover to find high-impact AI use cases for this work challenge: ...
   ```

Codex may also activate the skill implicitly when a request clearly asks to discover, compare, prioritize, or sharpen AI use cases.

## Three user actions

### Quick Find

Provide a challenge, desired outcome, task, workflow, KPI, role, decision point, or document context. CoDiscover returns up to three context-specific candidate use cases and a recommended next step.

### Quick Compare

Provide two to five existing ideas. CoDiscover compares context fit, four-dimensional value, readiness, risks, evidence gaps, and the smallest useful test.

### Quick Sharpen

Provide one broad or tool-led idea. CoDiscover reframes it at workflow level and adds human roles, AI roles, boundaries, checkpoints, evidence, and an MTUC.

## Example

```text
Use $codiscover to help with this challenge:
Our cross-functional team holds many meetings, but decisions are slow,
ownership becomes unclear after handoffs, and important follow-ups are lost.
```

Expected output characteristics:

- a concise Context Snapshot;
- no more than three materially different use cases in Quick Find;
- explicit facts, assumptions, and unknowns;
- separate Productivity, Impact, Inclusion, and Innovation profiles;
- a non-AI alternative;
- a transparent recommendation;
- a decision-ready MTUC with human accountability.

## Validate structured output

CoDiscover can return human-readable Markdown or schema-aligned JSON. Validate JSON with:

```text
python plugins/codiscover/skills/codiscover/scripts/validate_output.py path/to/output.json
python plugins/codiscover/skills/codiscover/scripts/critical_gate_check.py path/to/output.json
```

Run the repository QA suite with:

```text
python tests/run_qa.py
```

## Repository map

- `plugins/codiscover/` — installable Plugin package
- `plugins/codiscover/skills/codiscover/` — reusable discovery workflow
- `examples/` — synthetic, redistribution-safe cases
- `tests/` — schema, critical-gate, and hygiene checks
- `docs/` — architecture, product contract, build log, and judge instructions

## Build Week provenance

CoDiscover builds on the founder's long-standing work in problem discovery, project design, inclusion, and Human–AI collaboration. During OpenAI Build Week, those ideas were transformed with Codex and GPT-5.6 into a new, coherent, installable, and testable product.

See [Build log](docs/build-log.md) for the implementation record and [Product contract](docs/product-contract.md) for the current boundary.

## Build Week submission materials

- [Devpost submission draft](docs/devpost-submission-draft.md)
- [Under-three-minute demo script](docs/demo-video-script.md)
- [GitHub and Devpost release checklist](docs/release-checklist.md)
- [Judge testing guide](docs/judge-testing.md)

The repository is an early Build Week prototype. Public claims should be updated only when supported by pilot or QA evidence.

## Responsible boundary

CoDiscover is an advisory design system. It does not make final organizational decisions, execute production workflows, infer carbon emissions from token counts, or replace accountable human review.

## License

Code and original project materials in this clean repository are licensed under the MIT License. Third-party or restricted source materials are not included.
