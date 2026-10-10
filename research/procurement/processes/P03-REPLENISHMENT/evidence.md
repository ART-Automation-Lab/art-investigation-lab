# P03 Evidence Register — Inventory Replenishment & Reorder Exceptions

**Owner:** Bhushan  
**Standard:** ART Procurement Research Standard v1.0  
**Research date:** 2026-10-09

## Evidence classification rule

- **E0:** unvalidated hypothesis.
- **E1:** public documentation verifies process/capability.
- **E2:** public source explicitly documents and quantifies an industry pain point.
- **E3:** identified practitioner testimony.
- **E4:** direct operational validation within a specific enterprise.

The entries below support **E1 only**. This file does not claim E2, E3 or E4 evidence. Quotes are short verbatim excerpts from the linked public pages; re-open the canonical page and verify the exact wording/version before external publication.

## Evidence register

| Evidence ID | Level | Source title and canonical URL | Verbatim quote / data point | Supports claim |
|---|---|---|---|---|
| EVD-P03-001 | E1 | SAP Help Portal — Reorder Point Planning: https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/5697b6535fe6b74ce10000000a174cb4.html | “In reorder point planning, procurement is triggered when the sum of plant stock and firmed receipts falls below the reorder point.” | CLM-P03-010 |
| EVD-P03-002 | E1 | Oracle — Min-Max Planning: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/famml/min-max-planning.html | “min-max planning suggests a new purchase requisition or movement request” | CLM-P03-011 |
| EVD-P03-003 | E1 | Oracle — Min-Max Planning: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/famml/min-max-planning.html | Listed attributes include “Fixed lot multiple” and “Minimum order quantity”. | CLM-P03-012 |
| EVD-P03-004 | E1 | Oracle — How Min-Max Planning Replenishment Quantities Are Calculated: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/famml/how-min-max-planning-replenishment-quantities-are-calculated.html | “order quantity = maximum quantity - total available quantity, adjusted for order quantity modifiers.” | CLM-P03-013 |
| EVD-P03-005 | E1 | SAP Help Portal — Reorder Point Planning: https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/5697b6535fe6b74ce10000000a174cb4.html | SAP lists “Safety stock”, “Average consumption”, and “Replenishment lead time” among values important for defining the reorder point. | CLM-P03-014 |

## Claims supported by these sources

| Claim ID | Claim | Classification | Evidence IDs | Boundary |
|---|---|---|---|---|
| CLM-P03-010 | SAP documents a reorder-point trigger using plant stock plus firmed receipts. | Fact — E1 | EVD-P03-001 | Does not prove a particular customer uses this configuration. |
| CLM-P03-011 | Oracle min-max planning can suggest a purchase requisition or movement request when configured inventory is below minimum. | Fact — E1 | EVD-P03-002 | Output depends on configuration and planning source. |
| CLM-P03-012 | Oracle documents MOQ and fixed lot multiple as planning attributes. | Fact — E1 | EVD-P03-003 | Does not establish how frequently these attributes cause exceptions. |
| CLM-P03-013 | Oracle documents order-quantity calculation with order modifiers. | Fact — E1 | EVD-P03-004 | Calculation should be validated against the specific configuration. |
| CLM-P03-014 | SAP identifies safety stock, average consumption and replenishment lead time as relevant planning values. | Fact — E1 | EVD-P03-005 | Does not quantify the impact of lead-time variation in a specific enterprise. |

## Unvalidated hypotheses (E0)

| Claim ID | Hypothesis | Evidence required before promotion |
|---|---|---|
| CLM-P03-001 | Stale or contradictory inventory inputs create manual investigation work. | Identified practitioner testimony and direct operational examples. |
| CLM-P03-002 | MOQ/lot-multiple constraints frequently trigger planner intervention. | Exception logs with denominators and time window; item parameters; practitioner corroboration. |
| CLM-P03-003 | ART read-only analysis could reduce investigation effort. | Baseline time study and controlled test with predefined success criteria. |
| CLM-P03-004 | A target enterprise has a gap not already covered by its incumbent planning tools. | Installed module/configuration audit and observed workflow walkthrough. |

## Source and provenance limitations

- Target ERP and organization: **UNKNOWN**.
- Enterprise SOPs, audit logs and transaction records: **NOT PROVIDED**.
- Practitioner interviews: **NOT PROVIDED**.
- E2 benchmark with a verifiable quantitative pain metric: **NOT ESTABLISHED** in this package.
- E3 and E4: **NOT ACHIEVED**.
- ART test results: **UNTESTED**.

Do not promote evidence levels automatically. Record any source conflicts as separate claims and open ambiguity records rather than averaging results.

## Lab observations (not enterprise evidence)

> [!NOTE]
> **Epistemic boundary:** The observations below were obtained during testing on a synthetic laboratory instance (ERPNext on Frappe Cloud `bixbytessolutions.m.frappe.cloud`, company Aiotrix) between 2026-10-09 and 2026-10-10. These observations do NOT constitute enterprise operational evidence and carry **no E-level** (not E3 or E4). They represent technical environment verifications on synthetic test fixtures.

### 1. Synthetic test fixture parameters
- **Environment:** Frappe Cloud (`bixbytessolutions.m.frappe.cloud`), company Aiotrix.
- **Item Master:** `P03-TEST-ITEM-001` in warehouse `Stores - A`.
- **Initial Inbound Receipt:** Material Receipt `MAT-STE-00001` added 22 units at valuation rate 1.00 each.
- **Stock Balance Report:** Confirms actual balance 22, reserved 0, valuation 22.
- **Configured Item Reorder Rule:** Reorder level 50, reorder quantity 100, request type `Purchase`. Planning attributes `min_order_qty: 0`, `safety_stock: 0`, `lead_time_days: 0`.
- **Open Purchase Order Record:** `PUR-ORD-2026-00012` (submitted, status `To Receive and Bill`, transaction date 2026-10-10, schedule date 2026-10-10, item `P03-TEST-ITEM-001`, quantity 100, received quantity 0, warehouse `Stores - A`, rate and total 0 as test document).
- **Linked Material Request Record:** `MAT-MR-2026-00001` (status `Ordered`, type `Purchase`, transaction date 2026-10-10, schedule date 2026-10-10), linked to `PUR-ORD-2026-00012` via item `material_request` field.

### 2. Reconciled inventory observations
- **Reconciliation:** Current stock (22) + open purchase order (100 from `PUR-ORD-2026-00012`, not yet received, due 2026-10-10) = 122, exactly matching `projected_qty 122` returned by stock queries.
- **Position against Reorder Point:** Against the configured reorder level of 50, physical stock alone exhibits a deficit of 28 units. However, when factoring in open incoming supply (100 units), total inventory position is 122 units, resulting in a net shortage of 0.
- **Agent Design Implication:** The agent must inspect and report open purchase orders and pending replenishment requests before determining shortage, and must never suggest a new replenishment order when existing open supply covers the gap.
- **Unresolved Data Point:** Initial run of `get_tem_stock - ERPNext` returned `actual_qty: 22`, `reserved_qty: 0`, `ordered_qty: 0`, `projected_qty: 122`. Because this run occurred before purchase order `PUR-ORD-2026-00012` was confirmed and has not been repeated, the `ordered_qty` of 0 alongside `projected_qty` 122 is observed as an unexplained timing artifact and remains unresolved until re-tested (`AMB-P03-006`).

### 3. Tool execution observations
- **Tool Provider:** `erpnext_p03_v2` with 8 published read-only tools. (Older providers `erpnext_art` and `erpnext_p03` show 0 tools).
- **Stock Queries:** `get_tem_stock - ERPNext` and `find_inventory_across_warehouses` verified matching stock levels (22 actual, 0 reserved, 122 projected).
- **Reorder Level Lookup:** `Get Item Reorder Level` returned the full item document containing the configured reorder row (`Stores - A`, level 50, qty 100, `Purchase`); ignored warehouse filter.
- **Open Supply Lookups:** `find_replenishment_requests` returned `MAT-MR-2026-00001` (`Ordered`). `list_open_purchase_orders` returned `PUR-ORD-2026-00012` (`To Receive and Bill`) and correctly omitted unrelated item order `PUR-ORD-2026-00011` (`P02-TEST-ITEM-001`).
- **Order Details:** `get_po_details` verified line item linkage from `PUR-ORD-2026-00012` to `MAT-MR-2026-00001`.
- **Shortage Calculation:** Rebuilt inline function step for `calculate_inventory_shortages` was verified in function-step testing (inputs: 22 actual, 0 reserved, 50 reorder level, 0 incoming -> status `ok`, usable 22, position 22, shortage 28, shortage `true`, suggested qty 28). Published tool run from tool page was not captured. Run with incoming quantity 100 was not captured (hand calculation: position 122, shortage 0).
- **Agent Execution Status:** Agent "P03 Replenishment Exception Investigator" has been built in Agent Lab, but has NOT been run. Playground runs: none.
- **Data Privacy Invariant:** Strict privacy observed: only document identifiers, statuses, item codes, quantities, and dates are recorded. Personal names, telephone numbers, email addresses, supplier contact details, and system credentials have been omitted.
