# Capability Gaps & Central Ambiguities: P04 Invoice Discrepancy Resolution

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Process Owner:** Ashwin (`ashwinash19`)  
> **Central Register Reference:** [`../../AMBIGUITIES.md`](../../../AMBIGUITIES.md)  
> **Creation Date:** 2026-10-09  
> **Taxonomy:** Ambiguity Severities `A1` (Minor), `A2` (Material), `A3` (Critical), `A4` (Fatal / Safety)

---

## 1. Technical Capability Gaps

| Gap ID | Component / Area | Description | Impact on P04 Agent | Recommended Remediation |
|---|---|---|---|---|
| `GAP-P04-001` | **OCR / PDF Ingestion** | Zero PDF parsing, OCR engines, or document upload endpoints exist in repository or provider. | Agent cannot ingest raw vendor invoices directly; requires pre-structured ERPNext records. | Classify `WF-P04-001` as upstream pre-requisite; conduct validation on structured DocTypes. |
| `GAP-P04-002` | **Generic Create Tool (`DEF-P04-001`)** | `erpnext_create_docs_list` wraps input into `{"description": "{params.data}"}` with ToDo schema. | Blocks tool-based programmatic creation of ERPNext business documents via ART. | Keep tool excluded from agent; create controlled test records in ERPNext Desk UI or fix mapping. |
| `GAP-P04-003` | **Receipt Creation Tool (`DEF-P04-002`)** | `create_purchase_receipt` hardcodes supplier to `"MediSupply Healthcare Pvt Ltd"`. | Fails or corrupts validation if Purchase Order uses any other supplier. | Prohibit tool from P04 testing until refactored with dynamic supplier parameter. |
| `GAP-P04-004` | **Browser Service Constraint** | Automated browser execution encountered external `503 No capacity available` model limit. | Blocks automated browser subagent navigation of Desk. | Use Assisted Owner Setup in Desk UI ([bixbytessolutions.m.frappe.cloud/app](https://bixbytessolutions.m.frappe.cloud/app)). |

---

## 2. Central Ambiguity Ledger for P04

| Ambiguity ID | Severity | Description | Current Status | Required Action / Owner Decision |
|---|---|---|---|---|
| `AMB-P04-001` | **`A2` (Material)** | **Uncalibrated Tolerance Limits:** Corporate price and quantity variance tolerance limits before placing AP holds are not documented. | `OPEN` | Process Owner Ashwin to confirm initial tolerance threshold (recommended: $0.00 / 0% strict match). |
| `AMB-P04-002` | **`A3` (Critical)** | **Master Data State Post-Cleanup:** Unknown which master records survived demo data wipe. | **`RESOLVED`** | Empirically resolved on 2026-10-09: Live records verified: `P02 Test Supplier`, `P02-TEST-ITEM-001`, `PUR-ORD-2026-00011`, `PR-26-00001`, and `PINV-26-00007`. |
| `AMB-P04-003` | **`A4` (Safety)** | **Workflow Scope Boundary Contradiction:** `WF-P04-006` proposes payment release, conflicting with out-of-scope Treasury boundary. | `OPEN` | Process Owner Ashwin to confirm that `WF-P04-006` is a handoff and the agent terminates at recommendation. |

---

## 3. Required Owner Decisions Checklist

- [x] **Decision 1 (Master Setup):** Live master records and transaction records verified in ERPNext (`P02 Test Supplier`, `PUR-ORD-2026-00011`, `PR-26-00001`, `PINV-26-00007`).
- [ ] **Decision 2 (Tolerance Boundary):** Confirm that candidate agent must treat any non-zero price variance as an exception (`0.00 INR` tolerance).
- [ ] **Decision 3 (Treasury Boundary):** Formally approve restricting agent authority to producing audit dossiers and dispute recommendations, excluding payment release execution.
- [ ] **Decision 4 (Three-Way Match Execution):** Authorize agent execution of initial 3-way match comparison across `PUR-ORD-2026-00011` vs `PR-26-00001` vs `PINV-26-00007`.
