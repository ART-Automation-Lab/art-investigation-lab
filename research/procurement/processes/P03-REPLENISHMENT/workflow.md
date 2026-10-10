# P03 Workflow — Inventory Replenishment & Reorder Exceptions

**Owner:** Bhushan  
**Scope:** Read-only inventory replenishment exception investigation  
**Status:** Operational workflow aligned with Agent Lab tool provider `erpnext_p03_v2`; agent build status: BUILT BUT NOT RUN; scenario validation status: UNTESTED

## 1. Boundary

This workflow investigates replenishment planning inputs and produces an evidence-backed exception report. It does not create or release requisitions, purchase orders, supplier messages, inventory adjustments or planning-parameter changes. The workflow is strictly read-only (all HTTP interactions are GET operations; zero write tools are attached).

## 2. Operational workflow steps

The workflow executes as a sequential read-only pipeline using the published tools from provider `erpnext_p03_v2`:

### WF-P03-001 — Query stock position and multi-location balances
- **Action:** Query the inventory position for the specified item and warehouse.
- **Tools Attached:** `get_tem_stock - ERPNext` (item-warehouse stock inquiry) and `find_inventory_across_warehouses` (multi-location stock distribution).
- **Extracted Fields:** `actual_qty`, `reserved_qty`, `ordered_qty`, `projected_qty`.
- **Tool-Level Verification Status:** VERIFIED (confirmed on item `P03-TEST-ITEM-001` in `Stores - A`: actual 22, reserved 0, projected 122).
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).
- **Operational Boundary:** Read-only GET query; no stock adjustment or reservation mutation permitted.

### WF-P03-002 — Retrieve configured item reorder parameters
- **Action:** Retrieve the replenishment rule and reorder thresholds configured on the item master.
- **Tool Attached:** `Get Item Reorder Level`.
- **Extracted Fields:** `reorder_levels` (warehouse, reorder level, reorder qty, material request type), `min_order_qty`, `safety_stock`, `lead_time_days`.
- **Tool-Level Verification Status:** VERIFIED (confirmed on `P03-TEST-ITEM-001`: level 50, qty 100, `Purchase`). Known limitation: warehouse parameter is ignored by tool (returns full Item document with all reorder rows).
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).

### WF-P03-003 — Query open purchase orders and incoming supply details
- **Action:** Inspect open purchase orders for the target item and warehouse to establish confirmed incoming supply.
- **Tools Attached:** `list_open_purchase_orders` (queries orders with status `"To Receive and Bill"` and `"To Receive"`) and `get_po_details` (retrieves line-item quantities, schedule dates, and document linkages).
- **Incoming Supply Calculation Rule:**
  $$\text{incoming quantity} = \text{ordered quantity} - \text{received quantity}$$
  evaluated specifically on the matching item row within the purchase order.
- **Document Linkage Rule:** Link an existing replenishment material request to its corresponding purchase order through the order item's `material_request` field when present.
- **Tool-Level Verification Status:** VERIFIED AFTER FIX (filtering and Returns pointer fixes verified on `PUR-ORD-2026-00012`: qty 100, received 0, linked to `MAT-MR-2026-00001`).
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).

### WF-P03-004 — Inspect existing replenishment requests
- **Action:** Query pending material requests to identify already triggered replenishment requisitions.
- **Tool Attached:** `find_replenishment_requests` (queries open requests filtered by `item_code` and `warehouse`).
- **Extracted Fields:** request name (`MAT-MR-...`), `status`, `material_request_type`, transaction date, schedule date.
- **Tool-Level Verification Status:** VERIFIED AFTER FIX (item and warehouse filtering verified on `MAT-MR-2026-00001`, status `Ordered`).
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).

### WF-P03-005 — Calculate inventory position and evaluate shortage
- **Action:** Calculate net usable stock, total inventory position, and replenishment shortage against configured thresholds.
- **Tool Attached:** `calculate_inventory_shortages` (published as shortage calculator, rebuilt as serverless function step mapping 6 parameters from `${params.*}`).
- **Calculation Logic:**
  - $\text{usable inventory} = \text{actual\_qty} - \text{reserved\_qty}$
  - $\text{inventory position} = \text{usable inventory} + \text{incoming quantity}$
  - $\text{shortage} = \max(0, \text{reorder\_level} - \text{inventory position})$
  - If $\text{shortage} > 0$, evaluate MOQ and lot multiple rounding rules. If incoming supply covers the reorder point ($\text{inventory position} \ge \text{reorder\_level}$), $\text{shortage} = 0$ and no order recommendation is generated.
- **Tool-Level Verification Status:** PARTLY VERIFIED (verified at function-step test with inputs: actual 22, reserved 0, reorder level 50, incoming 0 -> position 22, shortage 28; run of published tool from tool page and run with incoming 100 NOT CAPTURED).
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).

### WF-P03-006 — Check transfer availability across warehouses and deliver report
- **Action:** Check if alternative warehouse locations hold surplus stock that could satisfy a deficit before external procurement; assemble final diagnostic report.
- **Tool Attached:** `check_transfer_availability`.
- **Tool-Level Verification Status:** `check_transfer_availability` is VERIFIED (returns stock row; known limitation: ignores `required_qty` and does not check reorder levels). Final report delivery is NOT CAPTURED (Playground runs: none).
- **Report Delivery:** Deliver structured exception report with Status `OK`, `INCOMPLETE`, or `NEEDS HUMAN REVIEW`. Include closing disclaimer that the report is diagnostic and not an order recommendation.
- **Agent Execution Status:** The agent implementing this step has NOT been run (Playground runs: none).

## 3. Exception paths and stop conditions

| Workflow ID | Trigger | Required response | Stop condition & Routing |
|---|---|---|---|
| WF-P03-007 | Missing item/location or ambiguous identity | Report unresolved identity | No calculation; Stop |
| WF-P03-008 | Stale or missing inventory/supply data | Flag freshness/data gap | No recommendation; Stop |
| WF-P03-009 | Conflicting source values | Preserve both values and source provenance | Stop; Human resolves authority |
| WF-P03-010 | MOQ/lot multiple or unit mismatch | Show documented rule and calculation only if verified | Stop if unit conversion/rule unclear |
| WF-P03-011 | Canceled/unconfirmed supply record | Apply only approved status rules | Stop if status semantics unknown |
| WF-P03-012 | Access denied/API error/partial result | Log error and mark report incomplete | No silent fallback; Stop |
| WF-P03-013 | Repeated run/retry | Reconcile read-only run metadata | No write action exists in scope |
| WF-P03-014 | Projected quantity does not equal actual + ordered - reserved and difference cannot be explained from returned data | Flag unexplained projected quantity anomaly and log mathematical discrepancy | Stop calculation; route to NEEDS HUMAN REVIEW |
| WF-P03-015 | A request has status Ordered but no matching open PO is found, or a PO is found whose quantity cannot be read | Flag supply order reconciliation anomaly and log missing/unreadable order | Stop calculation; route to NEEDS HUMAN REVIEW |

## 4. Human touchpoints

Human review is required when:
- Stop conditions `WF-P03-014` or `WF-P03-015` trigger;
- a planning parameter or data source is disputed;
- the source status is not understood;
- the proposed interpretation conflicts with an approved policy;
- an item is subject to special handling, sourcing, legal or financial restrictions;
- the agent cannot reproduce the result;
- a user asks for any write action outside this scope.

Detailed human review routing, policy rules, and timeout blocking behaviors are specified in [`./governance.md`](./governance.md).

## 5. Cross-process handoffs
- **P02:** supplier delivery status and lead-time information may be an input; P03 does not own supplier escalation.
- **P04:** goods receipt/invoice discrepancies are outside scope; P03 may mark supply records as uncertain if approved source data indicates a discrepancy.
- **P01:** approved sourcing or tender constraints may be consumed as inputs; P03 does not interpret tender obligations.

## 6. Audit record
Each run should retain, subject to approved retention policy:
- run identifier and timestamp;
- requester and authorization context;
- source system and query/read scope;
- input record identifiers and timestamps;
- rule/configuration version;
- calculation trace and unit conversions;
- exception classification;
- output and error state;
- human reviewer disposition, if collected.

Do not store credentials, secrets or unnecessary personal/supplier-confidential information in the report.

## 7. Validation status
All workflow steps are **UNTESTED** at the scenario level until exercised in an approved non-production environment against a reviewed expected result. The agent implementing this workflow has been built in Agent Lab but has NOT been run.
