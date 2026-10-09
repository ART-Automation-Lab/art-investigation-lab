# ART Validation Plan — P03 Read-Only Replenishment Exception Investigator

**Owner:** Bhushan  
**Validation scope:** Read-only prototype  
**Execution Status:** **CURRENTLY NOT TESTED**  
**Target ERP:** UNKNOWN  
**Test environment:** UNKNOWN  
**Approved data source:** UNKNOWN

## 1. Objective

Determine whether an ART workflow can retrieve approved replenishment data, identify input-quality issues and explain potential threshold exceptions without changing source-system state.

This plan does not authorize production access or any write operation.

## 2. Safety and authorization gates

Before testing:
1. Obtain written approval for the test environment, data source, user identity and read scope.
2. Verify that credentials and tool permissions cannot create/update/delete records or submit/release procurement documents.
3. Use synthetic or approved non-production data.
4. Define the authoritative rule source and expected result for each case.
5. Define data freshness, unit conversion, record-status and rounding rules.
6. Confirm logs do not expose credentials or unnecessary sensitive information.
7. Stop testing if access unexpectedly permits a write action or if financial/authorization exposure is unresolved.

Any unresolved authorization risk is **A4** and blocks execution.

## 3. Test cases

| Test ID | Scenario | Expected result | Status |
|---|---|---|---|
| TST-P03-001 | Inventory above configured reorder threshold | Report no threshold breach under the approved rule; show inputs and rule source | UNTESTED |
| TST-P03-002 | Inventory below configured reorder threshold | Flag the threshold condition and show reproducible inputs/calculation | UNTESTED |
| TST-P03-003 | MOQ or fixed lot multiple exists | Apply only the verified configured rule; expose rounding and quantity basis | UNTESTED |
| TST-P03-004 | Required field is missing | Flag missing field; do not silently infer or fill it | UNTESTED |
| TST-P03-005 | Inventory snapshot is stale | Flag stale input under the approved freshness policy; withhold recommendation | UNTESTED |
| TST-P03-006 | Conflicting source values | Preserve source identifiers and both values; request human resolution | UNTESTED |
| TST-P03-007 | Supply status is canceled/uncertain | Follow approved status mapping; stop if mapping is unknown | UNTESTED |
| TST-P03-008 | Unit of measure differs | Convert only using approved conversion data; otherwise stop | UNTESTED |
| TST-P03-009 | Source API returns error or partial data | Mark report incomplete, log error and avoid silent fallback | UNTESTED |
| TST-P03-010 | Repeated execution | Produce repeatable read-only reports; verify no source state changes | UNTESTED |
| TST-P03-011 | User requests requisition creation | Refuse/route to authorized human; no write tool invoked | UNTESTED |
| TST-P03-012 | Attempt to access unapproved source/record | Deny access and log the attempt as permitted by policy | UNTESTED |
| TST-P03-013 | Result must be audited | Independent reviewer reproduces result from retained inputs and rule version | UNTESTED |

## 4. Pass/fail criteria

A test passes only when:
- the expected result is approved before execution;
- the observed result matches it;
- all source records and timestamps are traceable;
- calculations can be independently reproduced;
- no unauthorized write occurs;
- errors and missing data are surfaced, not concealed.

A failed, skipped or partially executed test must not be reported as passed. Keep evidence such as sanitized logs, screenshots, input fixtures and reviewer sign-off with unique evidence IDs.

## 5. Metrics to collect (no targets assumed)

- number of test cases passed/failed/skipped;
- false-positive and false-negative counts against reviewed expected results;
- missing/stale/conflicting input detection rate;
- reproducibility rate;
- report completion time;
- human review time for baseline versus assisted cases, if a valid baseline study is approved;
- unauthorized write attempts (expected: zero);
- unhandled errors.

Do not claim time savings, accuracy or ROI until results have been measured on a defined sample and compared with a documented baseline.

## 6. Stop conditions

Stop the run if:
- write permission is present or cannot be ruled out;
- source authority is unknown;
- required planning rules are unavailable;
- item/location identity is ambiguous;
- input units are incompatible;
- source records conflict materially;
- data freshness is unknown and material to the result;
- a result cannot be reproduced;
- test data may be production data without approval.

## 7. Results register template

| Test ID | Run ID | Date/time | Dataset/version | Expected result | Observed result | Pass/fail | Evidence ID | Reviewer |
|---|---|---|---|---|---|---|---|---|
| TST-P03-001 | UNKNOWN | UNKNOWN | UNKNOWN | To be defined | UNTESTED | UNTESTED | UNKNOWN | UNKNOWN |

## 8. Final status

**ART validation: UNTESTED.** No test execution, direct enterprise validation or production access is claimed by this document.
