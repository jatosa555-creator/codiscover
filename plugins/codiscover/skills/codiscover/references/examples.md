# Calibration Examples

## Meeting-to-action

**Input:** Meetings are frequent, decisions are slow, handoffs are unclear, and follow-ups disappear.

**Strong behavior:** Frame the issue as decision continuity and handoff accountability. Compare a decision ledger, a handoff contract, and an assisted meeting-to-action workflow. Keep tentative statements separate from confirmed decisions. Test with a bounded set of meetings and named owners.

**Weak behavior:** Recommend a generic meeting summarizer and assume every detected action item is a commitment.

## Accounting document intake

**Input:** The team wants AI to process receipts and post transactions automatically.

**Strong behavior:** Separate assisted intake from bookkeeping authority. Recommend extraction, confidence flags, duplicate checks, an exception queue, reconciliation, and human approval. Test normal, duplicate, incomplete, unreadable, and conflicting documents. Do not recommend autonomous posting in the first test.

**Weak behavior:** Treat OCR accuracy as sufficient authorization to post transactions.

## Sensitive feedback triage

**Input:** Mixed-language employee feedback must be categorized and escalated quickly.

**Strong behavior:** Surface confidentiality, bias, false negatives, access controls, appeal, and missing-language risks. Preserve a non-AI reporting path. Use human review for high-severity and uncertain cases.

**Weak behavior:** Optimize only classification speed or assume sentiment scores are neutral.

## No-AI option

**Input:** A small team repeatedly forgets a two-step approval.

**Strong behavior:** Compare AI assistance with a checklist, form rule, or workflow configuration. Recommend the simpler intervention if it can solve the problem reliably.

**Weak behavior:** Add an agent because the request mentions AI.
