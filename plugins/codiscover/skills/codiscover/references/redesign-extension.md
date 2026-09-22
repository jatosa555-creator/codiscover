# ReDesign Extension

ReDesign is an optional Deep Design extension for CoDiscover. It is used after a candidate has been selected, or when the user explicitly asks to redesign a task, workflow, or operating model. The extension preserves the Core output and adds a traceable redesign layer.

## Design unit

Name the unit being redesigned before proposing an intervention: a task, handoff, decision, workflow, role, service, or operating model. Keep the boundary small enough that a human owner can inspect the change and reverse it.

## As-Is X-ray

Describe the current system before discussing AI:

- current work and sequence;
- waste, friction, duplication, waiting, and rework;
- necessary work that must remain;
- decisions and decision rights;
- evidence already available;
- constraints, affected people, and unknowns.

## Lean before agents

Separate four questions:

1. What work is waste and can be removed?
2. What work is necessary and should be simplified?
3. Where are the decision points and human checkpoints?
4. What capability would be added after the flow is made clear?

An agent is an option inside the redesigned flow, not the starting assumption. Always keep a non-AI path visible in the parent candidate use case.

## Three routes

Produce two or three materially different routes:

- **Enhance** — improve the existing flow with a bounded assist;
- **Redesign** — change the sequence, handoff, decision structure, or ownership;
- **Reimagine** — create a new capability or operating model when the old boundary is the main constraint.

For every route state the efficiency gain, the new capability created, human role, AI role, risks, evidence needed, and minimum experiment. Efficiency gain and new capability are separate claims; one does not imply the other.

## Decision-gate trace

Represent the route as Road, Junction, Checkpoint, Sensor, U-turn, and Exit points where useful. Every gate names:

- current state and available evidence;
- success conditions and constraints;
- options;
- a human decision owner and checkpoint;
- next action;
- the condition for a U-turn and the condition for exit.

The output remains advisory. Do not authorize autonomous execution or production integration from a ReDesign trace.

## Stop rule

Stop when the next decision and minimum experiment are clear. Do not force all routes or gates into the visible answer when the evidence does not support them.
