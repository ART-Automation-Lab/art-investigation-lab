# P03 Read-Only Agent: Governance Setup Guide

> **Process ID:** `P03-REPLENISHMENT`  
> **Process Name:** Inventory Replenishment & Reorder Exceptions  
> **Process Owner:** Bhushan  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)  
> **Validation Plan:** [`./art-validation.md`](./art-validation.md)  
> **Operational Workflow:** [`./workflow.md`](./workflow.md)  
> **Status:** Agent built in Agent Lab (`InvestigationLab` / `Testing`), but NOT run (Playground runs: none); Agent Lab Governance (Action Registry, Policy Rules, Human Review) is **not recorded**; scenario test status: `UNTESTED`  
> **Date:** 2026-10-09 to 2026-10-10  

---

## 1. Architectural Summary & Context

This guide defines the governance configuration, attached tool allowlist, system prompt rules, and target guardrail architecture for the **P03 Replenishment Exception Investigator** (Read-Only Agent) in **ART Agent Lab**.

### Epistemic Grounding & Core Safety Invariants:
1. **Strictly Read-Only Scope:** The agent is designed purely as an analytical diagnostic tool. It collects inventory snapshots, validates input data quality, flags configured reorder threshold breaches, and delivers an auditable report. It is **never** authorized to perform write actions (such as generating purchase requisitions, creating purchase orders, updating stock balances, or dispatching supplier messages).
2. **Fail-Closed Default:** If any uncertainty, data conflict, stale snapshot, or write attempt is encountered, execution immediately halts or transfers to a human planner.
3. **Defense-in-Depth:** Agent Lab governance policy rules operate as an application-level guardrail. Primary enforcement remains the read-only ERP/ERPNext API role (returning HTTP 403 on any state modification; see open ambiguity `AMB-P03-005`).
4. **Current Implementation Status:** The agent has been built on the board in Agent Lab (workspace `InvestigationLab`, environment `Testing`), but has NOT been run. Agent Lab governance features (Action Registry, Policy Rules, Human Review) were **not recorded** as configured for this agent.

---

## 2. Agent Board Architecture & Tool Allowlist

The agent board in Agent Lab connects three functional nodes:

```text
[ Model Node: Openai/Gpt-5.4 ] ────► [ Prompt Node: ERP-P03 ]
                 │
                 ▼
[ Tool Connector Node (8 Tools from erpnext_p03_v2) ]
```

### 2.1 Model Node Configuration
- **Model:** `Openai/Gpt-5.4`
- **Capabilities:** 13 capabilities enabled.
- **Unverified Risk:** The list of those 13 enabled capabilities was **NOT captured**. Some capabilities may allow actions outside the 8 attached tools.

### 2.2 Published Tool Allowlist (Tool Connector Node)
The Tool Connector node attaches exactly **8 published, read-only tools** from provider `erpnext_p03_v2`. Every HTTP operation is a `GET` step; zero create, update, submit, or delete tools exist. (The older providers `erpnext_art` and `erpnext_p03` now show 0 tools).

| # | Tool Display Name | Canonical Identifier | Provider | HTTP Method | Scope / Function |
|---|---|---|---|---|---|
| 1 | Find Inventory Across Warehouses | `find_inventory_across_warehouses` | `erpnext_p03_v2` | GET | Multi-warehouse stock balance distribution |
| 2 | Calculate Inventory Shortage | `calculate_inventory_shortages` | `erpnext_p03_v2` | Read-only Compute | Function-step shortage calculator |
| 3 | Get Item Reorder Level | `Get Item Reorder Level` | `erpnext_p03_v2` | GET | Item master reorder level and rules |
| 4 | Find Replenishment Requests | `find_replenishment_requests` | `erpnext_p03_v2` | GET | Open material requests (`MAT-MR-...`) |
| 5 | Get Item Stock | `get_tem_stock - ERPNext` | `erpnext_p03_v2` | GET | Item-warehouse stock position query |
| 6 | Check Transfer Availability | `check_transfer_availability` | `erpnext_p03_v2` | GET | Multi-location transfer stock availability |
| 7 | List Open Purchase Orders | `list_open_purchase_orders` | `erpnext_p03_v2` | GET | Open purchase orders (`PUR-ORD-...`) |
| 8 | Get PO Details | `get_po_details` | `erpnext_p03_v2` | GET | Purchase order line-item and request linkage |

> [!IMPORTANT]
> **Zero Write Tools Attached:**  
> No write tools (e.g. `create_purchase_requisition`, `submit_po`, `update_stock`) are attached or available in provider `erpnext_p03_v2`.

### 2.3 System Prompt Rules (Summary Form)
The Prompt node contains a system prompt constructed in the ERP-P02 style (titled `ERP-P03`). Its governing rules in summary form:
1. **Strictly Read-Only:** Refuse any user request to create, update, submit, or delete documents or alter system state without calling a tool.
2. **No Value Guessing:** Never guess, estimate, or extrapolate any numerical quantity, date, or threshold; name the specific tool source for every reported value.
3. **Empty Result Semantics:** An empty or null result from a tool means "nothing found", never numerical zero.
4. **Mandatory Anomaly Flagging:** Must proactively flag: missing values, reserved quantity exceeding actual physical stock, conflicting values across sources, unit of measure differences, unclear or unmapped order statuses, a material request with status `Ordered` lacking a matching open purchase order, and unexplained projected quantities.
5. **Privacy Enforcement:** Never repeat personal names, telephone numbers, email addresses, supplier contact details, or credentials from tool outputs.
6. **Structured Reporting Format:** Conclude with a deterministic status classification: `Status: OK`, `Status: INCOMPLETE`, or `Status: NEEDS HUMAN REVIEW`.
7. **Diagnostic Disclaimer:** End with an explicit closing disclaimer stating that the report is diagnostic only and is not a purchase order recommendation.
8. **Repository Storage Note:** *Full prompt text not stored in the repository.*

---

## 3. Agent Lab Governance Configuration (Status: Not Recorded)

> [!NOTE]
> **Implementation Status: Not Recorded.**  
> In the built agent board captured on 2026-10-10, native Agent Lab governance modules (**Action Registry**, **Policy Rules**, **Human Review**) were **NOT configured** (recorded as "not recorded").  
> The sections below specify the target governance architecture required to enforce fail-closed controls before production execution.

### 3.1 Proposed Action Registry
In Agent Lab, an agent may only execute actions explicitly declared and permitted in its **Action Registry**. Exactly **one** read-only custom action is specified:

| Parameter | Configuration Value | Description / Governance Purpose |
|---|---|---|
| **Action Identifier** | `p03.report_replenishment_exception` | Canonical identifier invoked when the agent generates an exception report. |
| **Display Name** | Report Replenishment Exception | Human-readable title displayed in logs and audit traces. |
| **Action Category** | `Custom` | User-defined diagnostic reporting action. |
| **Risk Classification** | `Low` | Read-only reporting action with zero financial or transactional mutation. |
| **Execution Mode** | `Sync` (Synchronous) | Ensures deterministic, blocking evaluation before report handoff. |
| **Required Facts** | `DATA_COMPLETE`, `REQUIRES_HUMAN_REVIEW` | Mandatory facts that must be populated before action execution. |
| **Allowed Side-Effects** | `NONE` (Zero Write Operations) | Strictly forbids ERP document creation, modification, or deletion. |

---

## 4. Fact Library Definition (Target Specification)

The **Fact Library** contains variables and flags evaluated by Policy Rules and routed into Human Review approval steps:

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

## 5. Policy Rules Specification (Target Specification)

Agent Lab evaluates **Policy Rules** sequentially in descending **Priority Order**, where the **first matching rule wins**:

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

## 6. Human Review Workflow Configuration (Target Specification)

When a Policy Rule resolves to `ASK_HUMAN`, Agent Lab triggers the **Human Review** approval flow:

| Review Setting | Configured Value | Operational Justification |
|---|---|---|
| **Approver Group** | `Inventory Planners` | Domain experts qualified to evaluate replenishment stock positions and supplier lead times. |
| **Approval Mode** | `Any one` | Fast triage: any authorized planner in the group can review and clear or reject the item. |
| **Timeout Duration** | `4 hours` | Standard operational shift window for replenishment exception resolution. |
| **Timeout Policy** | `BLOCK` (Fail-Closed) | **Critical safety gate:** If planners do not respond within 4 hours, the action terminates with `BLOCKED`. Never auto-approves or proceeds silently. |
| **Notification Channels** | `In-App`, `Push`, `Email` | Multi-channel dispatch to ensure prompt visibility of critical stockout exceptions. |
| **Mandatory Rationale** | `Required Reason: true` | Approvers must submit an auditable textual explanation for approving or rejecting the exception report. |

---

## 7. Operational Cautions & Implementation Guardrails

1. **ERP Backend User Permissions (`AMB-P03-005`):**  
   Agent Lab governance is an application-layer control that does not substitute for backend authorization. The permissions of the API key's user are **unverified** (`AMB-P03-005`, severity `A4`). On the Frappe Cloud site, items and purchase orders were created by a normal user account; therefore, the API key credentials may not be strictly read-only. Primary backend restriction to HTTP `GET` remains mandatory.
2. **Model Node Capabilities Unverified:**  
   The 13 capabilities enabled on the agent's `Openai/Gpt-5.4` model node were not enumerated or captured. Unverified capabilities could theoretically permit actions outside the 8 attached tools.
3. **Governance Modules Not Recorded:**  
   Because native Agent Lab Policy Rules, Human Review, and Action Registry were not recorded as configured on the built agent, the agent currently relies entirely on prompt instructions and Tool Connector tool restrictions. Full governance configuration must be completed before running live tests.
4. **Epistemic Traceability:**  
   Every fact and rule condition mapped above corresponds directly to an unexecuted test scenario in [`art-validation.md`](./art-validation.md). Keep all test cases labeled as **UNTESTED** until empirical runs have been conducted and logged in the Agent Lab Playground.

---

## 8. Next Actions & Execution Checklist

- [x] Create agent board in Agent Lab: `P03 Replenishment Exception Investigator` (built in `InvestigationLab` / `Testing`).
- [x] Attach 8 published read-only tools from provider `erpnext_p03_v2`.
- [x] Configure system prompt in ERP-P03 style with strict read-only and diagnostic rules.
- [ ] Configure Governance tab $\rightarrow$ Action Registry $\rightarrow$ Register `p03.report_replenishment_exception` (not recorded).
- [ ] Populate Fact Library with the 10 operational facts (not recorded).
- [ ] Configure the 4 priority-ordered Policy Rules (not recorded).
- [ ] Configure Human Review workflow with `Inventory Planners`, `Any one`, `4h timeout`, and `Timeout Policy: Block` (not recorded).
- [ ] Enumerate and verify the 13 model node capabilities.
- [ ] Audit Frappe Cloud API key user permissions to ensure backend read-only enforcement (`AMB-P03-005`).
- [ ] Conduct initial test runs in Agent Lab Playground across test scenarios `TST-P03-001` through `TST-P03-013` (currently 0 runs).
