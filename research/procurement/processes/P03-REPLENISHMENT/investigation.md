# P03 — Investigation Report: Inventory Replenishment & Reorder Exceptions

**Process ID:** P03-REPLENISHMENT  
**Owner:** Bhushan  
**Research mode:** Public-source investigation plus ART workflow design and validation plan  
**Research date:** 2026-10-09  
**Standard:** ART Procurement Research Standard v1.0 ([`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md))  
**Enterprise/system under investigation:** UNKNOWN  
**Highest evidence level currently supported:** E1 (public process verification)  
**E2 status:** Not established for a specific quantified pain point in this report  
**E3 status:** Not achieved; no practitioner testimony supplied  
**E4 status:** Not achieved; no enterprise SOP, transaction log, or live walkthrough supplied  
**ART validation status:** UNTESTED

> **Epistemic boundary:** This report uses public product documentation to establish documented capabilities. It does not claim that any named product is deployed by the target organization, that any exception occurs at a particular frequency, or that ART has passed a test. Enterprise-specific details remain `UNKNOWN`.

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

## 8. Open ambiguities

See [`evidence.md`](./evidence.md) for source records and [`art-validation.md`](./art-validation.md) for tests. Initial open ambiguities:
- AMB-P03-001: target ERP/system unknown (A2).
- AMB-P03-002: authoritative data source and freshness unknown (A3).
- AMB-P03-003: approved replenishment rules and parameter ownership unknown (A3).
- AMB-P03-004: enterprise exception frequency and cost unknown (A2).
- AMB-P03-005: ART permissions, API contracts and read-only enforcement unknown (A4 if consequential access is possible).

## 9. Exit criteria

Do not claim enterprise validation until authorized primary evidence has been reviewed. Do not claim ART feasibility until the validation cases pass in an approved test environment. Preserve the process boundary and do not modify application contracts.
