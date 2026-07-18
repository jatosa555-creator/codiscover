const PATTERNS = {
  evidence_brief: {
    title: "Evidence brief",
    workflowChange: "Turn long or conflicting material into a traceable brief before a person acts.",
    humanRole: "Confirm the question, approve claims, and make the decision.",
    aiRole: "Extract claims, compare sources, expose conflicts, and draft the brief.",
    values: { productivity: "medium", impact: "high", inclusion: "medium", innovation: "medium" },
    tradeoff: "Faster synthesis can create false confidence if provenance is weak.",
    risk: "Missing or low-quality evidence may be presented too neatly.",
    nonAi: "Use a standard evidence template and peer review."
  },
  exception_queue: {
    title: "Exception queue",
    workflowChange: "Separate routine work from unusual or high-consequence cases that need attention.",
    humanRole: "Own thresholds, review escalations, and override routing.",
    aiRole: "Screen incoming cases, explain flags, and assemble an exception queue.",
    values: { productivity: "high", impact: "high", inclusion: "medium", innovation: "medium" },
    tradeoff: "Higher throughput depends on reliable escalation rules.",
    risk: "A poorly designed threshold can hide important cases.",
    nonAi: "Use sampling, checklists, and a manually maintained escalation queue."
  },
  decision_ledger: {
    title: "Decision ledger",
    workflowChange: "Preserve decisions, owners, rationale, dependencies, and review dates across conversations.",
    humanRole: "Confirm decisions, ownership, and any change in status.",
    aiRole: "Extract candidate decisions, link evidence, and maintain a reviewable draft ledger.",
    values: { productivity: "medium", impact: "high", inclusion: "medium", innovation: "medium" },
    tradeoff: "Useful continuity requires people to validate what becomes organizational memory.",
    risk: "A draft or disputed statement could be mistaken for an approved decision.",
    nonAi: "Maintain a shared decision log with a named recorder."
  },
  handoff_contract: {
    title: "Handoff contract",
    workflowChange: "Make the trigger, required inputs, acceptance criteria, owner, and next action explicit at each handoff.",
    humanRole: "Sending and receiving owners confirm acceptance and exceptions.",
    aiRole: "Check completeness, surface ambiguity, and draft the handoff package.",
    values: { productivity: "high", impact: "high", inclusion: "medium", innovation: "medium" },
    tradeoff: "More structure reduces ambiguity but can add friction to simple work.",
    risk: "The template may conceal a deeper ownership or incentive problem.",
    nonAi: "Adopt a shared definition-of-ready and acceptance checklist."
  },
  assisted_intake: {
    title: "Assisted intake",
    workflowChange: "Convert inconsistent incoming information into a consistent, reviewable intake record.",
    humanRole: "Verify critical fields and handle consent or sensitive exceptions.",
    aiRole: "Extract, normalize, ask for missing information, and draft the record.",
    values: { productivity: "high", impact: "medium", inclusion: "high", innovation: "medium" },
    tradeoff: "Lower input burden must not reduce informed consent or user agency.",
    risk: "Critical details may be inferred incorrectly from incomplete input.",
    nonAi: "Redesign the form and offer assisted human intake."
  },
  triage_route: {
    title: "Triage and route",
    workflowChange: "Prioritize incoming work and route it with an explanation and an appeal path.",
    humanRole: "Set priorities, approve policy, and own appeals and overrides.",
    aiRole: "Classify requests, recommend priority, and explain the proposed route.",
    values: { productivity: "high", impact: "high", inclusion: "medium", innovation: "medium" },
    tradeoff: "Speed and consistency can conflict with context-sensitive fairness.",
    risk: "Historical patterns can reproduce unequal access or priority.",
    nonAi: "Use transparent routing rules with manual review and sampling."
  },
  draft_review: {
    title: "Draft and review",
    workflowChange: "Create a first draft from approved inputs while keeping publication or execution behind a human checkpoint.",
    humanRole: "Set intent, review accuracy and tone, and approve use.",
    aiRole: "Generate the draft, flag uncertainty, and revise from feedback.",
    values: { productivity: "high", impact: "medium", inclusion: "medium", innovation: "low" },
    tradeoff: "Time saved in drafting can shift effort into verification.",
    risk: "Plausible errors may pass when review becomes superficial.",
    nonAi: "Use reusable templates, examples, and editorial review."
  },
  compare_challenge: {
    title: "Compare and challenge",
    workflowChange: "Generate materially different options and test assumptions before committing to one approach.",
    humanRole: "Choose criteria, weigh trade-offs, and make the final decision.",
    aiRole: "Develop alternatives, challenge assumptions, and expose dissent or missing evidence.",
    values: { productivity: "medium", impact: "high", inclusion: "high", innovation: "high" },
    tradeoff: "More options improve exploration but can delay commitment.",
    risk: "AI-generated diversity may still reflect the same hidden assumptions.",
    nonAi: "Run a structured premortem or independent option review."
  },
  knowledge_continuity: {
    title: "Knowledge continuity",
    workflowChange: "Preserve validated context across people, time, and AI agents without treating every artifact as truth.",
    humanRole: "Decide what becomes reusable memory and retire stale knowledge.",
    aiRole: "Summarize context, link sources, detect conflicts, and propose updates.",
    values: { productivity: "medium", impact: "high", inclusion: "high", innovation: "high" },
    tradeoff: "Continuity improves reuse but increases governance and maintenance needs.",
    risk: "Outdated or unauthorized context may persist and influence later work.",
    nonAi: "Use curated handover notes and scheduled knowledge reviews."
  },
  scenario_rehearsal: {
    title: "Scenario rehearsal",
    workflowChange: "Explore assumptions and consequences before a consequential commitment.",
    humanRole: "Select assumptions, interpret scenarios, and own the decision.",
    aiRole: "Generate contrasting scenarios, trace consequences, and surface sensitivities.",
    values: { productivity: "low", impact: "high", inclusion: "medium", innovation: "high" },
    tradeoff: "Useful exploration takes time and cannot predict the future.",
    risk: "Detailed scenarios may be mistaken for forecasts.",
    nonAi: "Facilitate a premortem and tabletop exercise."
  },
  accessibility_adaptation: {
    title: "Accessibility adaptation",
    workflowChange: "Offer equivalent ways to understand, contribute, and act across formats and channels.",
    humanRole: "Affected users validate usability, dignity, and the non-AI path.",
    aiRole: "Adapt language, format, pace, or modality while preserving meaning.",
    values: { productivity: "medium", impact: "high", inclusion: "high", innovation: "high" },
    tradeoff: "Adaptation increases reach but requires quality checks across formats.",
    risk: "Simplification or translation may remove essential nuance.",
    nonAi: "Provide human support and professionally designed accessible alternatives."
  },
  learning_loop: {
    title: "Learning loop",
    workflowChange: "Use observed outcomes and feedback to improve a workflow through explicit review cycles.",
    humanRole: "Interpret evidence and decide whether to continue, revise, or stop.",
    aiRole: "Aggregate feedback, detect patterns, and propose testable changes.",
    values: { productivity: "medium", impact: "high", inclusion: "high", innovation: "high" },
    tradeoff: "Continuous learning requires measurement discipline and protected reflection time.",
    risk: "Easy-to-measure signals may crowd out meaningful outcomes.",
    nonAi: "Run regular retrospectives with a decision and experiment log."
  }
};

const FAMILY_RULES = [
  { words: ["meeting", "ประชุม", "decision", "ตัดสินใจ", "coordination", "ประสาน"], keys: ["decision_ledger", "handoff_contract", "knowledge_continuity"] },
  { words: ["document", "report", "เอกสาร", "รายงาน", "research", "ข้อมูล", "evidence"], keys: ["evidence_brief", "draft_review", "knowledge_continuity"] },
  { words: ["request", "intake", "ticket", "คำขอ", "แบบฟอร์ม", "volume", "จำนวนมาก", "queue"], keys: ["assisted_intake", "triage_route", "exception_queue"] },
  { words: ["handoff", "ส่งต่อ", "owner", "เจ้าของ", "workflow", "กระบวนการ"], keys: ["handoff_contract", "decision_ledger", "learning_loop"] },
  { words: ["option", "compare", "scenario", "ทางเลือก", "เปรียบเทียบ", "คาดการณ์", "strategy", "กลยุทธ์"], keys: ["compare_challenge", "scenario_rehearsal", "evidence_brief"] },
  { words: ["access", "inclusive", "inclusion", "เข้าถึง", "ความหลากหลาย", "ภาษา", "disability"], keys: ["accessibility_adaptation", "assisted_intake", "learning_loop"] },
  { words: ["quality", "error", "review", "คุณภาพ", "ผิดพลาด", "ตรวจสอบ", "risk", "ความเสี่ยง"], keys: ["draft_review", "exception_queue", "learning_loop"] }
];

const DEFAULT_KEYS = ["evidence_brief", "handoff_contract", "learning_loop"];

function compact(text, max = 120) {
  const normalized = String(text ?? "").replace(/\s+/g, " ").trim();
  return normalized.length > max ? `${normalized.slice(0, max - 1)}…` : normalized;
}

function selectPatternKeys(text, count = 3) {
  const lower = String(text ?? "").toLowerCase();
  const scored = new Map();
  for (const rule of FAMILY_RULES) {
    const hits = rule.words.filter((word) => lower.includes(word.toLowerCase())).length;
    if (!hits) continue;
    rule.keys.forEach((key, index) => scored.set(key, (scored.get(key) ?? 0) + hits * 10 - index));
  }
  const ranked = [...scored.entries()].sort((a, b) => b[1] - a[1]).map(([key]) => key);
  for (const key of DEFAULT_KEYS) if (!ranked.includes(key)) ranked.push(key);
  return ranked.slice(0, count);
}

function candidateFromPattern(key, challenge) {
  const pattern = PATTERNS[key];
  return {
    id: key,
    title: pattern.title,
    workflow_change: pattern.workflowChange,
    fit_to_challenge: `Apply this pattern to: ${compact(challenge)}.`,
    human_role: pattern.humanRole,
    ai_role: pattern.aiRole,
    value_profile: pattern.values,
    key_tradeoff: pattern.tradeoff,
    principal_risk_or_gap: pattern.risk,
    non_ai_alternative: pattern.nonAi,
    readiness: "Explore"
  };
}

function baseContext(input) {
  return {
    challenge: compact(input.challenge, 500),
    desired_outcome: compact(input.desired_outcome || "Not yet confirmed", 300),
    work_system_boundary: compact(input.work_context || "People, AI tools or agents, decisions, inputs, handoffs, and affected participants around this challenge.", 400),
    facts: [compact(input.challenge, 300)],
    assumptions: ["The challenge describes a work-system friction, not a preselected technology solution."],
    unknowns: ["Current baseline, consequence of failure, data sensitivity, decision owner, and affected voices are not yet confirmed."],
    confidence: "medium"
  };
}

export function discoverUseCases(input) {
  const keys = selectPatternKeys(`${input.challenge} ${input.desired_outcome ?? ""} ${input.work_context ?? ""}`);
  const candidates = keys.map((key) => candidateFromPattern(key, input.challenge));
  const first = candidates[0];
  const challenge = compact(input.challenge, 240);
  return {
    schema_version: "codiscover-chat-v0.1",
    action: "Quick Find",
    response_instructions: "Present this as decision support in the user's language. Keep facts, assumptions, and unknowns distinct. Do not invent ROI, baselines, consent, or evidence. The human owner makes the decision.",
    context_snapshot: baseContext(input),
    candidate_use_cases: candidates,
    recommendation: {
      status: "conditional",
      candidate_id: first.id,
      title: first.title,
      why_now: "It offers a bounded workflow change with an explicit human checkpoint and can be tested before broader automation.",
      why_not_other_first: "The alternatives remain useful, but the first test should reduce the most immediate uncertainty without combining multiple patterns.",
      most_important_uncertainty: "Whether this workflow change improves a meaningful outcome without shifting hidden burden or risk to other people.",
      next_safe_action: "Confirm one human owner and one observable baseline, then run a small reversible test."
    },
    minimum_testable_use_case: {
      hypothesis: `For a bounded sample of “${challenge}”, ${first.title} will improve one agreed outcome while keeping final accountability with a named person.`,
      scope_and_sample: "Use a small, representative, reversible sample; do not connect autonomous production actions.",
      human_owner: "To be named before testing",
      human_checkpoints: ["Approve inputs and boundaries", "Review every output in the pilot", "Make the Go / Revise / Stop decision"],
      data_boundary: "Use the minimum necessary data; exclude sensitive or unauthorized data until rights and controls are confirmed.",
      baseline: "Measure the current workflow before the pilot; do not estimate it retrospectively.",
      success_signals: ["Improvement in the chosen outcome", "Acceptable review effort and error rate", "No material loss of access, agency, or appeal"],
      failure_signals: ["Outputs cannot be reliably reviewed", "Burden or risk shifts to less-visible participants", "The non-AI process performs as well with lower cost or risk"],
      go_criteria: "Observed benefit, manageable risk, named ownership, and evidence strong enough for the next bounded test.",
      revise_criteria: "Some value is visible but workflow, data, checkpoint, or inclusion design needs adjustment.",
      stop_criteria: "Critical rights, safety, accountability, or feasibility gate fails, or no meaningful benefit appears.",
      review_point: "After the predefined sample, before any expansion"
    },
    responsibility_check: [
      "Confirm data rights, privacy, and provenance.",
      "Name the human decision owner and autonomy ceiling.",
      "Provide an appeal, fallback, and usable non-AI path.",
      "Check who gains value, who bears review work, and whose voice is missing.",
      "Prefer the least resource-intensive test that can reduce the key uncertainty."
    ],
    provenance: {
      user_confirmed: [compact(input.challenge, 300)],
      ai_inferred: ["Pattern fit, candidate ranking, and pilot design"],
      unknown: ["Baseline, stakeholders, data classification, evidence strength, and owner"]
    },
    next_decision: "Which candidate should be tested first, and who will own the final decision?"
  };
}

export function sharpenUseCase(input) {
  const discovered = discoverUseCases({
    challenge: input.idea,
    desired_outcome: input.desired_outcome,
    work_context: input.work_context
  });
  const selected = discovered.candidate_use_cases[0];
  return {
    schema_version: "codiscover-chat-v0.1",
    action: "Quick Sharpen",
    response_instructions: discovered.response_instructions,
    original_idea: compact(input.idea, 500),
    sharpened_use_case: {
      actor: "The person or role responsible for the outcome; confirm before testing.",
      trigger: "A real instance of the stated work challenge enters the bounded pilot.",
      inputs: "Only approved, minimum-necessary inputs for the selected sample.",
      workflow_change: selected.workflow_change,
      human_role: selected.human_role,
      ai_role: selected.ai_role,
      decision: "The named human owner decides whether and how the output is used.",
      output: `${selected.title} output linked to source inputs and uncertainty.`,
      checkpoint: "Human review before any consequential use.",
      intended_value: selected.value_profile
    },
    key_tradeoff: selected.key_tradeoff,
    responsibility_check: discovered.responsibility_check,
    minimum_testable_use_case: discovered.minimum_testable_use_case,
    next_decision: "Confirm the actor, baseline, and consequence of failure before running the test."
  };
}

export function compareUseCases(input) {
  const normalized = input.candidates.map((idea, index) => {
    const key = selectPatternKeys(idea, 1)[0];
    const card = candidateFromPattern(key, idea);
    return { ...card, id: `candidate_${index + 1}`, original_idea: compact(idea, 500) };
  });
  return {
    schema_version: "codiscover-chat-v0.1",
    action: "Quick Compare",
    response_instructions: "Compare these options in the user's language without collapsing Productivity, Impact, Inclusion, and Innovation into one total score. Treat pattern-based profiles as hypotheses to validate, not measured performance.",
    context_snapshot: {
      desired_outcome: compact(input.desired_outcome || "Not yet confirmed", 300),
      work_context: compact(input.work_context || "Not yet confirmed", 400),
      facts: input.candidates.map((idea) => compact(idea, 300)),
      assumptions: ["Each idea can be reframed as a workflow-level intervention."],
      unknowns: ["Baseline, evidence, affected people, data rights, and consequence of failure."]
    },
    normalized_candidates: normalized,
    recommendation_rule: "Prefer the option that can reduce the most important uncertainty through a bounded, reversible test with explicit human accountability. Hold when a critical responsibility gate is unresolved.",
    responsibility_check: ["Data rights and privacy", "Human owner and decision rights", "Inclusion and non-AI path", "Fallback and reversibility", "Resource proportionality"],
    next_decision: "Which trade-off matters most in this context, and who has the authority to decide?"
  };
}

export const internals = { PATTERNS, selectPatternKeys };
