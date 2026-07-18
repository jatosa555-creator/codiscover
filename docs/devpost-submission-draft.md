# Devpost Submission Draft

> Working draft for OpenAI Build Week. Review all claims, replace pending links, and run the release checklist before final submission.

## Project name

CoDiscover

## Tagline

Turn a real work challenge into a responsible, prioritized, and testable Human–AI use case.

## Category

Work and productivity

## Short description

CoDiscover is an installable ChatGPT and Codex plugin that helps a person, team, or organization discover and compare high-value AI opportunities from real work challenges. Instead of stopping at an idea list, it produces a Minimum Testable Use Case with explicit human accountability, evidence signals, checkpoints, and Go/Revise/Stop criteria.

## Inspiration

Organizations often begin AI adoption with a tool or a generic list of use cases. That creates many ideas but weak problem fit, unclear ownership, and little evidence that a proposed workflow will create meaningful value.

CoDiscover began with a different question: how can people discover AI opportunities from real work while considering productivity, impact, inclusion, and innovation together? The product combines the founder's experience in problem discovery, project design, inclusive practice, and Human–AI collaboration with the implementation capabilities of Codex and GPT-5.6.

## What it does

CoDiscover supports three fast actions:

- **Quick Find:** generate up to three materially different use cases from a challenge, workflow, KPI, role, decision, or document context.
- **Quick Compare:** compare existing ideas across context fit, value, readiness, evidence gaps, and risk.
- **Quick Sharpen:** turn a broad or tool-led idea into a workflow-level Human–AI experiment.

The selected opportunity becomes a **Minimum Testable Use Case (MTUC)** that names the human owner, human and AI roles, boundaries, checkpoints, evidence, and decision criteria. A conditional retrieval layer can bring in external work patterns only when the user's context is too thin or comparison is explicitly requested.

## How it works

1. Capture a concise context snapshot and separate facts, assumptions, and unknowns.
2. Locate leverage points in the existing work system.
3. Generate a small set of context-specific Human–AI options, including a non-AI alternative.
4. Profile Productivity, Impact, Inclusion, and Innovation independently.
5. Recommend transparently, including uncertainty and evidence gaps.
6. Design the smallest responsible test with explicit human accountability.
7. Apply nine critical gates before recommending Go, Revise, or Stop.

## How we built it

Codex with GPT-5.6 was used throughout product synthesis, architecture, plugin scaffolding, skill specification, documentation engineering, validator implementation, and QA. The founder supplied the original perspective, domain synthesis, values, problem framing, product judgment, trade-offs, and final decisions.

The public repository was created as a clean-room implementation. It contains an installable plugin, a reusable skill, progressive reference files, a structured output contract, deterministic validators, synthetic examples, a judge testing guide, and an automated QA workflow. Confidential organizational materials, paid-course content, and unverified third-party materials are excluded.

## Challenges we ran into

- Preserving a broad "for all value-creating work" ambition without producing generic use cases.
- Keeping the user experience simple while retaining evidence, responsibility, and inclusion backstage.
- Distinguishing discovery from implementation so the first product remains coherent.
- Using external patterns as conditional inspiration rather than an always-on answer library.
- Translating a rich conceptual manual into a compact, installable, and testable plugin.

## Accomplishments we are proud of

- A working installable plugin rather than a prompt document.
- A four-value compass that does not reduce AI value to time savings alone.
- A decision-ready MTUC as the destination of discovery.
- Explicit human accountability and non-AI alternatives.
- Nine machine-checkable responsibility gates.
- A redistribution-safe repository with positive and negative QA fixtures.

## What we learned

The hardest part of AI adoption is often not generating an answer. It is discovering where intervention is justified, deciding how humans and AI should share the work, and designing evidence that supports a responsible next decision. Strong use-case discovery is therefore a form of work-system design, not merely brainstorming.

## What's next

- Run a bounded pilot across five workflow families.
- Improve scoring calibration and question selection from observed failure modes.
- Add evidence-backed conditional pattern retrieval.
- Explore a later handoff from Discover to Design and Build without turning the core plugin into an unfocused agent bundle.
- Measure whether CoDiscover improves decision quality, inclusion, and experiment readiness—not only speed.

## Technologies used

- ChatGPT and Codex
- GPT-5.6
- Codex Plugin and Skill specifications
- Python validation and QA scripts
- JSON Schema
- GitHub Actions

## Links required before final submission

| Item | Draft status |
|---|---|
| Public GitHub repository | https://github.com/jatosa555-creator/codiscover |
| Public YouTube demo under three minutes | Pending recording and upload |
| Primary Codex `/feedback` Session ID | Pending final session selection |
| Installation/test instructions | Complete in `README.md` and `docs/judge-testing.md` |
