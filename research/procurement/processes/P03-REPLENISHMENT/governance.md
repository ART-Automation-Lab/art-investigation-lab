# P03 Read-Only Agent: Governance Setup Guide

> **Process ID:** `P03-REPLENISHMENT`  
> **Process Name:** Inventory Replenishment & Reorder Exceptions  
> **Process Owner:** Bhushan  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)  
> **Validation Plan:** [`./art-validation.md`](./art-validation.md)  
> **Operational Workflow:** [`./workflow.md`](./workflow.md)  
> **Status:** Proposed Governance Architecture (`UNTESTED` / Pending Agent Lab Configuration)  
> **Date:** 9 October 2026  

---

## 1. Architectural Summary & Context

This guide defines the end-to-end governance configuration in **ART Agent Lab** for the proposed **P03 Replenishment Exception Investigator** (Read-Only Agent).

It adapts the proven design pattern observed in the production **Implant Usage Reconciliation Agent**'s Governance tab (comprising Action Registry, Fact Library, Policy Rules, and Human Review approval workflows). 

### Epistemic Grounding & Core Safety Invariants:
1. **Strictly Read-Only Scope:** The agent is designed purely as an analytical diagnostic tool. It collects approved inventory snapshots, validates input data quality, flags configured reorder threshold breaches, and delivers an auditable report. It is **never** authorized to perform write actions (such as generating purchase requisitions, creating purchase orders, updating stock balances, or dispatching supplier messages).
2. **Fail-Closed Default:** If any uncertainty, data conflict, stale snapshot, or write attempt is encountered, execution immediately halts or transfers to a human planner.
3. **Defense-in-Depth:** Agent Lab governance policy rules operate as an application-level guardrail. Primary enforcement remains the read-only ERP/ERPNext API role (returning HTTP 403 on any state modification, tracking open ambiguity `AMB-P03-005`).
4. **Current Status:** Inferred from Agent Lab UI specifications and architectural templates; **all rules and facts remain UNTESTED** until validated in the Agent Lab Playground.

---

## 2. Action Registry Configuration

In Agent Lab, an agent may only execute actions explicitly declared and permitted in its **Action Registry**. To enforce a strictly read-only posture, exactly **one** custom action is registered, with zero write actions permitted.

### Registered Action: `p03.report_replenishment_exception`

| Parameter | Configuration Value | Description / Governance Purpose |
|---|---|---|
| **Action Identifier** | `p03.report_replenishment_exception` | Canonical identifier invoked when the agent generates an exception report. |
| **Display Name** | Report Replenishment Exception | Human-readable title displayed in logs and audit traces. |
| **Action Category** | `Custom` | User-defined diagnostic reporting action. |
| **Risk Classification** | `Low` | Read-only reporting action with zero financial or transactional mutation. |
| **Execution Mode** | `Sync` (Synchronous) | Ensures deterministic, blocking evaluation before report handoff. |
| **Required Facts** | `DATA_COMPLETE`, `REQUIRES_HUMAN_REVIEW` | Mandatory facts that must be populated before action execution. |
| **Allowed Side-Effects** | `NONE` (Zero Write Operations) | Strictly forbids ERP document creation, modification, or deletion. |

> [!IMPORTANT]
> **Zero Write Actions Registered:**  
> Never register actions such as `p03.create_purchase_requisition`, `p03.submit_po`, or `p03.update_stock`. Because the agent's capability boundary is locked by the registry, the agent has no mechanism to attempt or execute transactions in the ERP.

---

## 3. Fact Library Definition

The **Fact Library** contains variables and flags evaluated by Policy Rules and routed into Human Review approval steps.

Unlike the generic Implant agent (which accumulated auto-generated parser fields), the P03 library is intentionally pruned to include only purposeful, test-mapped facts that directly mirror scenarios in [`art-validation.md`](./art-validation.md):

| Fact Identifier | Data Type | Default Value | Driving Test Case / Trigger | Description & Governance Function |
|---|---|---|---|---|
| `WRITE_REQUESTED` | `Boolean` | `false` | `TST-P03-011` | Set to `true` if prompt or upstream input requests requisition creation, PO dispatch, or state modification. |
| `DATA_COMPLETE` | `Boolean` | `false` | `TST-P03-004`, `TST-P03-009` | Set to `true` only if all mandatory fields (item ID, warehouse/location, on-hand qty, ROP) are present. |
| `SNAPSHOT_STALE` | `Boolean` | `false` | `TST-P03-005` | Set to `true` if inventory balance or open-supply timestamp exceeds enterprise freshness tolerance. |
| `SOURCE_CONFLICT` | `Boolean` | `false` | `TST-P03-006` | Set to `true` if conflicting stock balances or contradictory supply orders are detected across source systems. |
| `STATUS_MAPPING_KNOWN` | `Boolean` | `true` | `TST-P03-007` | Set to `false` if an open supply order carries an unrecognized, canceled, or unmapped status. |
| `UOM_CONVERSION_APPROVED` | `Boolean` | `true` | `TST-P03-008` | Set to `false` if item packaging unit differs from base inventory UOM without an approved conversion table. |
| `REQUIRES_HUMAN_REVIEW` | `Boolean` | `false` | Review Gate | Master evaluation flag indicating that human planner intervention is required before proceeding. |
| `ITEM_ID` | `String` | `""` | Traceability | Primary inventory item identifier under diagnostic review. |
| `LOCATION_ID` | `String` | `""` | Traceability | Warehouse, distribution center, or bin location under review. |
| `THRESHOLD_BREACHED` | `Boolean` | `false` | `TST-P03-001`, `TST-P03-002` | Set to `true` if effective stock is less than or equal to configured reorder point (ROP). |

---

## 4. Policy Rules Specification

Agent Lab evaluates **Policy Rules** sequentially in descending **Priority Order**, where the **first matching rule wins**. 

```text
[Incoming Action: p03.report_replenishment_exception]
                           │
                           ▼
          [Rule 1: WRITE_REQUESTED == true?]
                ├── YES ──► [OUTCOME: BLOCK / DENY] (Fail-Closed)
                └── NO
                     │
                     ▼
  [Rule 2: Any Input Quality Anomaly Detected?]
  (SNAPSHOT_STALE || SOURCE_CONFLICT || !DATA_COMPLETE || !STATUS_MAPPING_KNOWN || !UOM_CONVERSION_APPROVED)
                ├── YES ──► [OUTCOME: ASK HUMAN] (Route to Review Flow)
                └── NO
                     │
                     ▼
          [Rule 3: REQUIRES_HUMAN_REVIEW == true?]
                ├── YES ──► [OUTCOME: ASK HUMAN] (Route to Review Flow)
                └── NO
                     │
                     ▼
          [Rule 4: Standard Clean Diagnostic Report]
                └── [OUTCOME: ALLOW] (Generate Read-Only Report)
```

### Detailed Rule Set:

#### Rule 1: Write Attempt Interception (Priority: Highest / 1)
- **Target Action:** `p03.report_replenishment_exception` (and any unexpected action)
- **Condition:** `WRITE_REQUESTED == true`
- **Enforcement Outcome:** `BLOCK` (or `DENY`; if Agent Lab only supports `Ask Human`, route to human with explicit reject recommendation)
- **Rationale:** Intercepts any prompt injection or user attempt to trigger transactional purchases (`TST-P03-011`). Refuses write actions and prevents automated execution.

#### Rule 2: Input Integrity & Exception Triage (Priority: High / 2)
- **Target Action:** `p03.report_replenishment_exception`
- **Condition:**  
  `DATA_COMPLETE == false` **OR**  
  `SNAPSHOT_STALE == true` **OR**  
  `SOURCE_CONFLICT == true` **OR**  
  `STATUS_MAPPING_KNOWN == false` **OR**  
  `UOM_CONVERSION_APPROVED == false`
- **Enforcement Outcome:** `ASK_HUMAN` (Sets `REQUIRES_HUMAN_REVIEW = true`)
- **Rationale:** Prevents hallucinated or corrupted calculations when source data is compromised (`TST-P03-004` through `TST-P03-009`).

#### Rule 3: Explicit Human Review Gate (Priority: Medium / 3)
- **Target Action:** `p03.report_replenishment_exception`
- **Condition:** `REQUIRES_HUMAN_REVIEW == true`
- **Enforcement Outcome:** `ASK_HUMAN`
- **Rationale:** Captures edge cases or planner review overrides flagged by agent reasoning.

#### Rule 4: Clean Diagnostic Report Clearance (Priority: Low / 4)
- **Target Action:** `p03.report_replenishment_exception`
- **Condition:** Default / All upstream rules evaluate to `false`
- **Enforcement Outcome:** `ALLOW`
- **Rationale:** Formulates and outputs the clean read-only exception diagnostic to the approved planner interface.

---

## 5. Human Review Workflow Configuration

When a Policy Rule resolves to `ASK_HUMAN`, Agent Lab triggers the **Human Review** approval flow. P03 directly adopts the fail-closed parameters modeled in the Implant agent:

| Review Setting | Configured Value | Operational Justification |
|---|---|---|
| **Approver Group** | `Inventory Planners` | Domain experts qualified to evaluate replenishment stock positions and supplier lead times. |
| **Approval Mode** | `Any one` | Fast triage: any authorized planner in the group can review and clear or reject the item. |
| **Timeout Duration** | `4 hours` | Standard operational shift window for replenishment exception resolution. |
| **Timeout Policy** | `BLOCK` (Fail-Closed) | **Critical safety gate:** If planners do not respond within 4 hours, the action terminates with `BLOCKED`. Never auto-approves or proceeds silently. |
| **Notification Channels** | `In-App`, `Push`, `Email` | Multi-channel dispatch to ensure prompt visibility of critical stockout exceptions. |
| **Mandatory Rationale** | `Required Reason: true` | Approvers must submit an auditable textual explanation for approving or rejecting the exception report. |

---

## 6. Operational Cautions & Implementation Guardrails

1. **Rule Outcome Limitations in Agent Lab:**  
   In the Implant agent screenshot, `Ask Human` is the primary visible enforcement outcome. During setup in the Agent Lab UI, verify whether an explicit `Block` / `Deny` outcome exists for Rule 1 (`WRITE_REQUESTED`). If absent, configure `Ask Human` with a mandatory pre-filled rejection note.
2. **ERP-Level Role Isolation (`AMB-P03-005`):**  
   Agent Lab governance is an application-layer control. It does **not** replace backend infrastructure controls. The ERPNext / ERP API service user credentials provided to the agent must possess **exclusively Read-Only permissions** (e.g., `SELECT` / `GET` on `Item`, `Bin`, `Purchase Order Item`, with zero `INSERT`/`UPDATE`/`SUBMIT` permissions). A `403 Forbidden` response at the network layer remains the ultimate safeguard.
3. **Fact Hygiene:**  
   Do not blindly accept auto-generated output parser fields (such as `additionalProperties`, `case_id`, `reason_raw`). Maintain only clean, typed, documented facts in the P03 Fact Library to avoid catalog bloat and rule ambiguity.
4. **Epistemic Traceability:**  
   Every fact and rule condition mapped above corresponds directly to an unexecuted test scenario in [`art-validation.md`](./art-validation.md). Keep all test cases labeled as **UNTESTED** until empirical runs have been conducted and logged in the Agent Lab Playground.

---

## 7. Next Actions & Execution Checklist

- [ ] Open **Agent Lab** $\rightarrow$ Create Agent: `Replenishment Exception Investigator`.
- [ ] Navigate to **Governance** tab $\rightarrow$ Action Registry $\rightarrow$ Register `p03.report_replenishment_exception` (Low Risk, Sync).
- [ ] Add the 7 core operational facts to the **Fact Library** (`WRITE_REQUESTED`, `DATA_COMPLETE`, `SNAPSHOT_STALE`, `SOURCE_CONFLICT`, `STATUS_MAPPING_KNOWN`, `UOM_CONVERSION_APPROVED`, `REQUIRES_HUMAN_REVIEW`).
- [ ] Configure the 4 priority-ordered **Policy Rules** in the rule editor.
- [ ] Configure the **Human Review** flow with `Inventory Planners`, `Any one`, `4h timeout`, and `Timeout Policy: Block`.
- [ ] Conduct initial test runs in **Playground** against synthetic payloads to exercise `TST-P03-001` through `TST-P03-013`.
