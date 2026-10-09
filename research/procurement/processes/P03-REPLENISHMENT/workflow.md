# P03 Workflow — Inventory Replenishment & Reorder Exceptions

**Owner:** Bhushan  
**Scope:** Read-only inventory replenishment exception investigation  
**Status:** Proposed workflow; not a verified enterprise SOP; ART status UNTESTED

## 1. Boundary

This workflow investigates replenishment planning inputs and produces an evidence-backed exception report. It does not create or release requisitions, purchase orders, supplier messages, inventory adjustments or planning-parameter changes.

## 2. Workflow steps

### WF-P03-001 — Establish scope and authorized source
- Identify the approved inventory organization, location/subinventory, item and time horizon.
- Confirm the authorized source system and data access scope.
- If system, item or location identity is ambiguous, stop and request human clarification.
- **Evidence required:** approved source/system list and access authorization.
- **Status:** UNTESTED.

### WF-P03-002 — Read planning inputs
Read only fields explicitly approved for the test, where available:
- item and organization/location identifiers;
- on-hand/nettable quantity and unit of measure;
- firm/open supply quantities and statuses;
- applicable demand/reservations;
- configured reorder point or min/max thresholds;
- safety stock;
- lead time;
- MOQ, maximum order quantity and fixed lot multiple;
- source timestamps and record identifiers.

Do not assume every system exposes all fields or that field names are interchangeable. Record absent fields as `UNKNOWN`.

### WF-P03-003 — Validate data quality
Check:
- required fields present;
- identifiers resolve to one item and one location;
- units of measure are compatible;
- timestamps satisfy the approved freshness policy;
- supply records have statuses defined by the approved rules;
- no conflicting authoritative values exist.

If any critical check fails, produce a data-quality exception and do not calculate a consequential recommendation.

### WF-P03-004 — Evaluate configured trigger
- Use the incumbent system's documented/configured rule where available.
- Do not replace ERP logic with an assumed universal formula.
- Record the rule source/version and input snapshot.
- If configuration cannot be verified, label the result “illustrative only” and stop short of a business recommendation.

### WF-P03-005 — Explain the exception
For each flagged item, report:
- item/location identifiers;
- observed values and timestamps;
- configured threshold and source;
- relevant open supply/demand records included or excluded under the approved rule;
- calculation steps, units and rounding;
- missing/contradictory fields;
- why human review is required.

### WF-P03-006 — Deliver report for human review
- Produce a read-only report with stable claim/evidence IDs.
- Route it only to the approved recipient or test output location.
- Do not submit a requisition or make a source-system change.
- Record run ID, time, source version and errors.

## 3. Exception paths

| Workflow ID | Trigger | Required response | Stop condition |
|---|---|---|---|
| WF-P03-007 | Missing item/location or ambiguous identity | Report unresolved identity | No calculation |
| WF-P03-008 | Stale or missing inventory/supply data | Flag freshness/data gap | No recommendation |
| WF-P03-009 | Conflicting source values | Preserve both values and source provenance | Human resolves authority |
| WF-P03-010 | MOQ/lot multiple or unit mismatch | Show documented rule and calculation only if verified | Stop if unit conversion/rule unclear |
| WF-P03-011 | Canceled/unconfirmed supply record | Apply only approved status rules | Stop if status semantics unknown |
| WF-P03-012 | Access denied/API error/partial result | Log error and mark report incomplete | No silent fallback |
| WF-P03-013 | Repeated run/retry | Reconcile read-only run metadata | No write action exists in scope |

## 4. Human touchpoints
Human review is required when:
- a planning parameter or data source is disputed;
- the source status is not understood;
- the proposed interpretation conflicts with an approved policy;
- an item is subject to special handling, sourcing, legal or financial restrictions;
- the agent cannot reproduce the result;
- a user asks for any write action outside this scope.

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
All workflow steps are **UNTESTED** until exercised in an approved non-production environment against a reviewed expected result.
