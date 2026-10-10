# P03 — Investigation Report: Inventory Replenishment & Reorder Exceptions

**Process ID:** P03-REPLENISHMENT  
**Owner:** Bhushan  
**Research mode:** Public-source investigation plus ART workflow design and validation plan  
**Research date:** 2026-10-09  
**Standard:** ART Procurement Research Standard v1.0 ([`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md))  
**Enterprise/system under investigation:** UNKNOWN (Target enterprise ERP remains UNKNOWN; laboratory testing conducted on synthetic ERPNext instance on Frappe Cloud `bixbytessolutions.m.frappe.cloud`, company Aiotrix)  
**Highest evidence level currently supported:** E1 (public process verification)  
**E2 status:** Not established for a specific quantified pain point in this report  
**E3 status:** Not achieved; no practitioner testimony supplied  
**E4 status:** Not achieved; no enterprise SOP, transaction log, or live walkthrough supplied  
**ART validation status:** UNTESTED (Tools verified/partly verified in lab; Agent built in Agent Lab but NOT run; all 13 test scenarios remain UNTESTED)

> **Epistemic boundary:** This report uses public product documentation to establish documented capabilities. It does not claim that any named product is deployed by the target organization, that any exception occurs at a particular frequency, or that ART has passed a test. Enterprise-specific details remain `UNKNOWN`. Lab observations on synthetic Frappe Cloud data do NOT constitute enterprise evidence and carry no E-level.

## 1. Scope and boundary

### In scope
- Reorder-point and min-max planning concepts.
- Safety-stock threshold monitoring.
- Review of planning inputs, including available stock, firm receipts, demand, lead time, MOQ and lot multiples where supported by the incumbent system.
- Read-only replenishment exception investigation and evidence-backed reporting.
- A validation plan for a proposed ART read-only workflow.

### Out of scope
- Supplier acknowledgment, shipment tracking and delivery-delay escalation (P02).
- RFP/tender review and response coordination (P01).
- Invoice/receipt discrepancy resolution (P04).
- Purchase-order creation, release, supplier commitment, or any other consequential write action.
- Changes to `contracts/` or application schemas.

## 2. Executive summary

**Fact — E1:** SAP S/4HANA documentation describes reorder-point planning and explains that the reorder point should cover expected material requirements during replenishment lead time. Oracle Fusion Cloud SCM documentation describes min-max planning that can suggest a purchase requisition or movement request when the planning inventory level falls below a configured minimum. Sources: [SAP Reorder Point Planning](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/5697b6535fe6b74ce10000000a174cb4.html) and [Oracle Min-Max Planning](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/famml/min-max-planning.html).

**Inference:** Because incumbent planning products already implement standard replenishment calculations, an ART prototype should not be justified as a replacement calculation engine without evidence of a specific gap. A narrower read-only investigator could assemble source records, identify configured threshold breaches, flag inconsistent or stale inputs, and explain why a case needs human review.

**Unknown:** Target enterprise, ERP, item master configuration, actual exception frequency, planner workload, current manual steps, API availability, and business authorization model.

**Conclusion:** Proceed only with a read-only proof of concept using synthetic or approved non-production data. No autonomous write action is proposed.

## 3. As-is reference workflow (public baseline, not a verified company SOP)

1. **WF-P03-001 — Collect planning inputs:** obtain inventory position, firm receipts/open supply, applicable demand, planning parameters and source timestamps.
2. **WF-P03-002 — Evaluate trigger:** compare the relevant inventory measure against the configured reorder point or min-max minimum.
3. **WF-P03-003 — Determine suggested quantity:** apply the incumbent system's configured replenishment and order-modifier rules.
4. **WF-P03-004 — Inspect exceptions:** flag missing, stale, contradictory or out-of-scope inputs for human review.
5. **WF-P03-005 — Present evidence:** provide source identifiers, timestamps, rule applied, calculation basis and unresolved questions.
6. **WF-P03-006 — Hand off:** route the report to an authorized planner; ART does not create, submit, approve or release a request.

These are reference workflow steps derived from public product documentation and a proposed read-only design. They are not evidence of the target enterprise's actual operating procedure.

## 4. Incumbent software audit

### SAP S/4HANA
**Fact — E1:** SAP documents reorder-point planning and identifies safety stock, average consumption and replenishment lead time as important values. It also describes manual and automatic determination of reorder and safety-stock levels.
Source: [SAP Help Portal — Reorder Point Planning](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/5697b6535fe6b74ce10000000a174cb4.html).

**Limitation of current evidence:** This establishes documented capability, not the target organization's configuration or actual performance.

### Oracle Fusion Cloud SCM
**Fact — E1:** Oracle documents min-max planning using minimum and maximum quantities and supports attributes including minimum order quantity and fixed lot multiple. It may suggest purchase requisitions or movement requests depending on configuration.
Source: [Oracle — Min-Max Planning](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/famml/min-max-planning.html).

Oracle also documents calculation logic for available quantity and order quantity modifiers:
[Oracle — How Min-Max Planning Replenishment Quantities Are Calculated](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/famml/how-min-max-planning-replenishment-quantities-are-calculated.html).

### Other products
Coupa, JAGGAER, ServiceNow and Tipalti are not assessed as installed systems for the target organization. Their precise role, modules and deployment status are **UNKNOWN**. Do not infer that they replace an ERP planning engine.

## 5. Exception hypotheses (unvalidated; E0)

| Claim ID | Hypothesis | What would validate it |
|---|---|---|
| CLM-P03-001 | Planners may need to investigate stale or contradictory stock/supply inputs. | E3 interview plus E4 examples from authorized transaction records. |
| CLM-P03-002 | MOQ or lot-multiple rules may make a suggested quantity require review. | Approved item parameters and a traced replenishment case. |
| CLM-P03-003 | A read-only agent may reduce time spent assembling evidence for exceptions. | Baseline time study and controlled comparison; no savings claim before measurement. |
| CLM-P03-004 | Repeated runs or retries could create duplicate work if downstream controls are weak. | Architecture review and controlled idempotency/failure tests. |

No exception frequency, delay cost, financial impact or expected productivity improvement is claimed.

## 6. High-consequence failure modes to test

- **Financial:** incorrect quantity, inappropriate rounding, excess inventory, duplicate request.
- **Operational:** stockout risk misclassified because of stale or missing supply data.
- **Authorization:** read-only agent obtains or uses write permissions unexpectedly.
- **Auditability:** recommendation cannot be reconstructed from retained inputs and rule version.

Likelihood, severity and current controls are **UNKNOWN** pending enterprise evidence.

## 7. ART candidate assessment

**Candidate:** Read-only replenishment exception investigator.

**Allowed:** read approved data; compare values against approved rules; calculate a transparent diagnostic; identify missing/stale/conflicting fields; produce a report with evidence IDs; recommend human review.

**Forbidden in this scope:** create/update/delete inventory records; create or submit requisitions; approve/release orders; contact suppliers; alter planning parameters; infer missing values as facts.

**Stop conditions:** missing required inputs; incompatible units; ambiguous item/location identity; stale data beyond an approved threshold; conflicting authoritative records; unknown policy; permission error; failed source retrieval; non-deterministic or irreproducible calculation.

**Current validation status:** UNTESTED. See [`art-validation.md`](./art-validation.md).

## 8. Lab implementation findings

Testing and agent assembly were conducted on 2026-10-09 and 2026-10-10 using synthetic test fixtures on an ERPNext instance hosted on Frappe Cloud (`bixbytessolutions.m.frappe.cloud`, company Aiotrix). These findings document tool-level behavior, agent configuration, and environment observations. They are synthetic lab findings and do NOT constitute enterprise operational evidence.

### 8.1 Reconciled inventory finding
- **Observation:** On test fixture item `P03-TEST-ITEM-001` in warehouse `Stores - A`, actual physical stock is 22 (from receipt `MAT-STE-00001`). One open purchase order exists: `PUR-ORD-2026-00012` for 100 units (submitted, status `To Receive and Bill`, schedule date 2026-10-10, not yet received).
- **Projected Quantity Match:** Physical stock 22 + open PO 100 = 122, exactly reconciling with the `projected_qty: 122` returned by the stock tools and the ERPNext Stock Balance report.
- **Linkage to Material Request:** Purchase order `PUR-ORD-2026-00012` links directly to material request `MAT-MR-2026-00001` (`status: Ordered`) via the PO line item's `material_request` field.
- **Shortage Assessment:** The configured reorder level is 50. Considering physical on-hand stock alone, an apparent gap of 28 units exists (50 - 22). However, when factoring in the open purchase order of 100 units, the total inventory position is 122 units, which is 72 units above the reorder point, resulting in a net shortage of 0.
- **Architectural Consequence for the Agent:** The agent must inspect and report open purchase orders and pending replenishment requests before drawing any shortage conclusion. It must never propose or suggest a replenishment order when existing open supply already covers the deficit.
- **Residual Open Point:** Initial execution of `get_tem_stock - ERPNext` reported `actual_qty: 22`, `reserved_qty: 0`, `ordered_qty: 0`, and `projected_qty: 122`. Because this run occurred before purchase order `PUR-ORD-2026-00012` was confirmed and was not repeated, the order of events is not confirmed. This is logged as an unresolved timing point (`AMB-P03-006`) until `get_tem_stock` is re-run.

### 8.2 Agent build status
- **Agent Name & Location:** `P03 Replenishment Exception Investigator` was created in ART Agent Lab (workspace `InvestigationLab`, environment `Testing`). Role: read-only investigator for inventory replenishment exceptions.
- **Board Configuration:**
  - **Model Node:** `Openai/Gpt-5.4` with 13 capabilities enabled. The specific capabilities enabled were NOT captured.
  - **Tool Connector Node:** Exactly 8 tools attached from published read-only provider `erpnext_p03_v2` (`Find Inventory Across Warehouses`, `Calculate Inventory Shortage`, `Get Item Reorder Level`, `Find Replenishment Requests`, `Get Item Stock`, `Check Transfer Availability`, `List Open Purchase Orders`, `Get PO Details`).
  - **Prompt Node:** System prompt constructed in ERP-P02 style (title `ERP-P03`).
- **Prompt Rules Summary:** The prompt enforces strict read-only execution; refusal of any document creation or modification without invoking tools; prohibition against guessing values; explicit tool citation for every reported metric; treating empty results as "nothing found" rather than zero; mandatory flagging of missing values, reserved exceeding actual, conflicting sources, UOM variance, unclear order status, requests with status `Ordered` lacking an open PO, and unexplained projected quantity; prohibition on echoing personal or contact details; and a structured output status (`OK`, `INCOMPLETE`, `NEEDS HUMAN REVIEW`) ending with a diagnostic disclaimer. Full prompt text not stored in the repository.
- **Agent Lab Governance:** Policy Rules, Action Registry, and Human Review workflows were NOT configured on this agent as far as captured (recorded as "not recorded").
- **Execution Status:** The agent has been built but NOT run. No Playground runs have been captured.

### 8.3 Defects found and fixes
1. **Query Filter Omission in Supply Tools:** Early versions of `find_replenishment_requests`, `list_open_purchase_orders`, and `get_incoming_purchase_orders` omitted `item_code` and `warehouse` query parameters, and `list_open_purchase_orders` queried only status `"To Bill"`. Corrected in provider `erpnext_p03_v2` with item and warehouse filters and open statuses `"To Receive and Bill"` and `"To Receive"`.
2. **`get_po_details` Step Pointer and URL Space:** The Returns field pointed to a non-existent step (returning blank) and the URL contained an unencoded literal space. Fixed by re-mapping Returns to the active GET step and encoding the space as `%20`.
3. **Shortage Calculator Serverless Handler Failure:** Initial imported serverless-handler version of `calculate_inventory_shortages` consistently returned an empty string in live executions (`ok: true`, blank output) due to an unknown platform-side cause. Worked around by rebuilding the calculator as an inline function step mapping 6 parameters from `${params.*}`. Verified in function-step testing (position 22, shortage 28). The legacy handler copy must not be used.
4. **Missing Master Data (HTTP 404):** Queries for item codes `SKU008`, `SKU009`, and `SKU010` returned HTTP 404 (`DoesNotExistError`). These records were from a different test dataset and do not exist on the current Frappe Cloud instance. Updated to use verified item `P03-TEST-ITEM-001`.

### 8.4 Known tool limitations
1. **`check_transfer_availability`:** Ignores the `required_qty` input parameter and does not evaluate reorder thresholds.
2. **`Get Item Reorder Level`:** Returns the entire `Item` document containing all warehouse reorder rows, ignoring the `warehouse` input parameter.
3. **Indented Quantity:** Stock query endpoints do not expose indented (requested) material request quantities.

### 8.5 Risks and unverified items
1. **Coordination Risk with P02:** Open purchase orders on `P03-TEST-ITEM-001` utilize a test supplier created for P02 test data, creating an overlap risk between P02 and P03 test fixtures.
2. **Unverified Model Node Capabilities:** The 13 capabilities enabled on the agent's `Openai/Gpt-5.4` model node were not enumerated; some capabilities could theoretically permit actions outside the 8 read-only tools.
3. **API Key Authorization (`AMB-P03-005`):** Frappe Cloud API key permissions remain unverified at the backend user level.

## 9. Open ambiguities

See [`evidence.md`](./evidence.md) for source records and [`art-validation.md`](./art-validation.md) for tests. Open ambiguities:
- AMB-P03-001: target ERP/system unknown (A2). *Status:* Partly resolved for the synthetic lab test environment only (ERPNext on Frappe Cloud `bixbytessolutions.m.frappe.cloud`, company Aiotrix); enterprise target ERP remains UNKNOWN.
- AMB-P03-002: authoritative data source and freshness unknown (A3). *Status:* OPEN. Stock tools return no timestamp and no enterprise freshness policy exists; blocks `TST-P03-005`.
- AMB-P03-003: approved replenishment rules and parameter ownership unknown (A3). *Status:* OPEN. Status mapping for cancelled/unconfirmed orders (`TST-P03-007`) unapproved.
- AMB-P03-004: enterprise exception frequency and cost unknown (A2). *Status:* OPEN.
- AMB-P03-005: ART permissions, API contracts and read-only enforcement unverified (A4). *Status:* OPEN. The permissions of the API key's user are unverified. Items and orders on the Frappe Cloud site were created by a normal user account, so the API key may not be restricted to read-only access.
- AMB-P03-006: Residual `ordered_qty` discrepancy in `get_tem_stock` (A2). *Status:* OPEN. Initial execution of `get_tem_stock - ERPNext` returned `actual_qty: 22`, `reserved_qty: 0`, `ordered_qty: 0`, and `projected_qty: 122`. Because the run occurred before purchase order `PUR-ORD-2026-00012` was confirmed and was not repeated, the order of events (whether stock check occurred before or after PO submission) is unconfirmed. Remains unresolved until `get_tem_stock` is re-run and returns both `ordered_qty` and `projected_qty`.

## 10. Exit criteria

Do not claim enterprise validation until authorized primary evidence has been reviewed. Do not claim ART feasibility until the validation cases pass in an approved test environment. Preserve the process boundary and do not modify application contracts.
