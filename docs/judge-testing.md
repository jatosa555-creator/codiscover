# Judge Testing Guide

## Supported surfaces

- ChatGPT desktop app with Codex and local Plugin support
- Codex CLI with Plugin marketplace support

## Install

1. Clone or download this repository.
2. Add its marketplace root:

   ```text
   codex plugin marketplace add <absolute-path-to-codiscover-repository>
   ```

3. Install:

   ```text
   codex plugin add codiscover@personal
   ```

4. Restart the desktop app or open a new Codex task.

## Golden test

Invoke:

```text
Use $codiscover to help with this challenge:
Our cross-functional team holds many meetings, but decisions are slow,
ownership becomes unclear after handoffs, and important follow-ups are lost.
We need a low-risk first test and do not want autonomous production changes.
```

Expected behavior:

- no more than three Quick Find candidates;
- facts, assumptions, and unknowns remain separate;
- four independent value dimensions;
- explicit human and AI roles;
- non-AI alternatives;
- transparent recommendation and uncertainty;
- MTUC with owner, checkpoints, evidence, and Go/Revise/Stop criteria.

## Validate the included sample

From repository root:

```text
python plugins/codiscover/skills/codiscover/scripts/validate_output.py examples/meeting-to-action-output.json
python plugins/codiscover/skills/codiscover/scripts/critical_gate_check.py examples/meeting-to-action-output.json
python tests/run_qa.py
```

All commands should return exit code 0. The QA suite also confirms that an intentionally invalid fixture is rejected.

## Test the optional layers

The synthetic deep-design sample demonstrates the additive schema v0.2 contract:

```text
python plugins/codiscover/skills/codiscover/scripts/validate_output.py examples/redesign-meta-lab-output.json
python plugins/codiscover/skills/codiscover/scripts/critical_gate_check.py examples/redesign-meta-lab-output.json
```

Ask for ReDesign only after selecting a candidate, for example: “Redesign this workflow before adding an AI agent. Show the As-Is X-ray, Lean scan, routes, and decision gates.” Ask for Meta-Lab only when supplying at least two completed traces or experiments. Both layers should retain human owners, evidence, correction paths, and a minimum experiment.

## Known limitations

- The prototype advises and designs; it does not execute production workflows.
- No external course or organizational evidence is bundled.
- K3 external retrieval requires a separately authorized source.
- Output quality still depends on the clarity of available context and human review.
