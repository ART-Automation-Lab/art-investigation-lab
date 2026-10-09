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
