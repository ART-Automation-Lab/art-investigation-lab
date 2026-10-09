# ART Agent Validation: RFP Requirement Review & Response Coordination (P01-RFP)

> **Process ID:** `P01-RFP`  
> **Process Owner:** Chiranjeevi  
> **Execution Status:** **PARTIALLY VALIDATED / DEFECT DISCOVERED**  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)

---

## 1. Candidate ART Autonomous Capabilities

An autonomous ART agent in the tender requirement review domain is evaluated against five core operational criteria:
1. **Extraction Completeness:** Parsing complex, unstructured tender documents and extracting 100% of binding requirements without human omission.
2. **Obligation Grounding:** Accurately categorizing obligations as `MANDATORY` (`must`, `shall`) or `PREFERRED` (`should`, `may`).
3. **SME Ownership Suggestion:** Recommending cross-functional functional owners (Engineering, Security, Legal, Commercial) while explicitly maintaining that internal ownership is proposed, not verified.
4. **Epistemic Honesty:** Flagging supplier compliance answers as strictly `UNKNOWN` in the absence of internal capability evidence, preventing hallucinated compliance claims.
5. **Traceability & Line-Level Citations:** Providing verifiable page/section references for every extracted requirement.

---

## 2. Guardrails and Human-in-the-Loop (HIL) Constraints

- **No Autonomous Bid Submission:** The agent must never transmit bids or compliance answers directly to an external buyer portal.
- **SME Assignment Status:** All routing recommendations must be stamped `SUGGESTED_NOT_CONFIRMED`.
- **Compliance Default:** In the absence of primary organizational proof, compliance status for every requirement must remain strictly `UNKNOWN`.
- **Zero Hallucination Gate:** Immediate fail if any invented requirement or ungrounded citation is returned.

---

## 3. Synthetic Benchmark Protocol: RFP-001

A formal synthetic validation kit is established in [`../../validation/RFP-001/`](../../validation/RFP-001/):

- **Synthetic Test Document:** [`../../validation/RFP-001/RFP-001-Test-Document.md`](../../validation/RFP-001/RFP-001-Test-Document.md) (8-section enterprise tender containing 20 seeded requirements).
- **Agent Instruction Prompt:** [`../../validation/RFP-001/RFP-001-ART-Agent-Prompt.md`](../../validation/RFP-001/RFP-001-ART-Agent-Prompt.md) (Standard instruction set and JSON extraction contract).
- **Evaluation Checklist & Metrics:** [`../../validation/RFP-001/RFP-001-Test-Checklist.md`](../../validation/RFP-001/RFP-001-Test-Checklist.md).
- **Gold Reference Answer Key:** [`../../validation/RFP-001/RFP-001-Gold-Answer-Key.md`](../../validation/RFP-001/RFP-001-Gold-Answer-Key.md) *(Strictly isolated from tested agents)*.

---

## 4. Test Execution Summary

The following controlled validation executions have been conducted and logged in the local [`executions/`](./executions/) directory:

| Test Run ID | Execution Type | Target / Capability | Status | Evidence Record | Summary / Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TEST-P01-001` | Synthetic Benchmark | Extraction Fidelity on 20 Seeded Clauses | **PASS** | [`VAL-P01-001.md`](./executions/VAL-P01-001.md) | 20/20 requirements extracted; 17 mandatory, 3 preferred; zero hallucinations; all compliance set to UNKNOWN. |
| `TEST-P01-002` | Platform Runtime Test | Agent Lab "Configure Prompt" Editor UI | **FAIL** | [`VAL-P01-002.md`](./executions/VAL-P01-002.md) | Textarea recomposition glitch resets typing cursor to index 0 on periodic background re-render. Logged as defect. |
| `BUG-P01-001` | Defect Investigation | Caret Jump on Periodic Re-render | **FILED / SYNCED** | [`BUG-P01-001.md`](./executions/BUG-P01-001.md) | Logged via ART Bug Pipeline as canonical `ART-AGENT-010` / Azure Work Item `#69076` (detailed in [`BUG-P01-001.md`](./executions/BUG-P01-001.md)). |

---

## 5. Empirical Operational Validation Requirements (Future Gates)

Prior to enterprise deployment for live tender bidding:
1. **Multi-Format Ingestion:** Ingestion of messy multi-column scanned PDFs and encrypted Word tender exhibits.
2. **Ambiguity Calibration:** Demonstrating that contradictory client clauses trigger `A3` ambiguity warnings rather than forced extractions.
3. **Orchestrator Routing:** Live integration with ART Orchestrator to dispatch extracted clauses to verified enterprise SME channels.
