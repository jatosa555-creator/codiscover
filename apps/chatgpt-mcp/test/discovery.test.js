import test from "node:test";
import assert from "node:assert/strict";
import { compareUseCases, discoverUseCases, internals, sharpenUseCase } from "../discovery.js";

test("meeting challenge selects decision and handoff patterns", () => {
  const result = discoverUseCases({ challenge: "Meeting decisions are lost and nobody knows who owns the next handoff." });
  assert.equal(result.action, "Quick Find");
  assert.equal(result.candidate_use_cases.length, 3);
  assert.equal(result.candidate_use_cases[0].id, "decision_ledger");
  assert.ok(result.minimum_testable_use_case.human_checkpoints.length >= 3);
});

test("Thai intake challenge selects assisted intake", () => {
  const keys = internals.selectPatternKeys("คำขอจำนวนมากเข้ามาหลายแบบและแบบฟอร์มไม่ครบ");
  assert.equal(keys[0], "assisted_intake");
});

test("comparison preserves separate value dimensions", () => {
  const result = compareUseCases({ candidates: ["Summarize long reports", "Route incoming service requests"] });
  assert.equal(result.normalized_candidates.length, 2);
  assert.deepEqual(Object.keys(result.normalized_candidates[0].value_profile), ["productivity", "impact", "inclusion", "innovation"]);
});

test("sharpening keeps human decision checkpoint", () => {
  const result = sharpenUseCase({ idea: "Build an AI agent that automatically writes and sends every client report" });
  assert.match(result.sharpened_use_case.decision, /human owner/i);
  assert.match(result.sharpened_use_case.checkpoint, /Human review/i);
});
