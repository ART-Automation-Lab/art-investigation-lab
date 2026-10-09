# ART FEATURE PIPELINE — ORCHESTRATOR
VERSION: HARNESS 01 → HARNESS 02 AUTOMATIC HANDOFF FOR ENHANCEMENTS

## PURPOSE

Run the complete ART feature-processing workflow from one invocation.

This pipeline orchestrates the feature harnesses:

- **Harness 01**: ART FEATURE INTAKE & STORAGE HARNESS
- **Harness 02**: ART AZURE USER STORY TICKET HARNESS

The pipeline automatically passes a successfully stored canonical Feature Request from Harness 01 to Harness 02.

The user does NOT need to:
- manually locate the newly created feature folder
- attach the canonical feature folder
- paste the canonical Markdown again
- reattach the same evidence
- manually run Harness 02
- manually provide the Feature ID after Harness 01 finishes

This is an ORCHESTRATION layer only.
DO NOT merge Harness 01 and Harness 02 responsibilities.

---

## 1. INPUT

The user may provide:
- short/raw feature request or enhancement description
- screenshots or UI mockups
- existing behavior vs proposed behavior
- business impact and user experience
- target Module or product area
- related Bug IDs (e.g. `ART-AGENT-007`, Azure `#68933`)
- existing Feature ID for an update
- `LOCAL_ONLY: YES` flag

Harness 01 is responsible for structuring the feature request.

---

## 2. REQUIRED FLOW

```
RAW FEATURE REQUEST + EVIDENCE
        ↓
    HARNESS 01
        ↓
CANONICAL FEATURE STORED
        ↓
 READY FOR AZURE?
        ↓
       YES
        ↓
  READ FEATURE ID
        ↓
    HARNESS 02
        ↓
AZURE USER STORY CREATE / RECONCILE
        ↓
      VERIFY
        ↓
FINAL COMBINED RESULT
```

There is no manual stop between Harness 01 and Harness 02 when:
`READY FOR AZURE: YES` (unless `LOCAL_ONLY: YES`).

---

## 3. HARNESS 01 RESPONSIBILITIES

Harness 01 remains authoritative for:
- Feature ID allocation (`ART-FEAT-<MODULE>-###`)
- duplicate/update detection
- canonical Module resolution
- Classification (`NEW_FEATURE` vs `ENHANCEMENT`)
- Title, Problem/Opportunity, Proposed Behavior, Acceptance Criteria
- local evidence storage
- canonical Markdown creation under `features/<MODULE>/<FEATURE-ID>__<slug>/`
- feature ledger compilation (`ART_FEATURE_BACKLOG_LEDGER.md`)
- Azure readiness check

Do not independently allocate Feature IDs outside Harness 01.

---

## 4. HARNESS 02 RESPONSIBILITIES

Harness 02 remains authoritative for:
- Azure parent Feature resolution under Epic `Backlog Tickets` (#69099)
- verification of Epic #69099 hierarchy
- Azure duplicate detection using `ART:<FEATURE-ID>` tag
- Azure User Story creation (`$User Story`)
- existing-ticket reconciliation
- Acceptance Criteria and Description projection
- evidence attachments with duplicate prevention
- post-sync Azure readback verification
- canonical Azure metadata writeback (`Azure Work Item ID: #<id>`, `Azure Sync Status: SYNCED`)

---

## 5. AZURE HIERARCHY CONTRACT

- **Organization:** `BixBytesSolutions`
- **Project:** `ART IPR-0063`
- **Epic:** `Backlog Tickets` (#69099)
- **Module Features (Parent Work Items):**
  1. Agent Lab (#69102)
  2. Orchestrator (#69103)
  3. Tool Builder (#69104)
  4. MCP Servers (#69105)
  5. Triggers (#69106)
  6. Credential Manager (#69107)
  7. Serverless Functions (#69108)
  8. Governance (#69109)
  9. Human-in-the-Loop / Approvals (#69110)
  10. Live Connect (#69111)
  11. ART Development Kit (ADK) (#69112)
  12. Agent X (#69113)
- **Work Item Type:** `User Story`

---

## 6. FAILURE SAFETY

- **If Harness 01 fails:** STOP. Never attempt Azure synchronization.
- **If Harness 02 fails:** STOP. Do NOT create duplicate User Stories. Keep the canonical feature stored locally with `Azure Sync Status: FAILED` and report the exact blocker.

---

## 7. LOCAL_ONLY MODE

When `LOCAL_ONLY: YES`:
- Run Harness 01 only.
- Do not run Harness 02.
- Return local storage path and feature ID with status `LOCAL_ONLY_COMPLETE`.

Default is `LOCAL_ONLY: NO`.

---

## 8. FINAL USER-FACING OUTPUT

### Success
```text
PIPELINE: COMPLETE
FEATURE ID: ART-FEAT-<MODULE>-###
TITLE: <title>
MODULE: <Module>
CLASSIFICATION: NEW_FEATURE / ENHANCEMENT
LOCAL STORAGE: STORED
LEDGER: UPDATED
AZURE USER STORY: CREATED / EXISTING
WORK ITEM: #<Azure ID>
AZURE PARENT FEATURE: <Feature Name> (#<Feature ID>)
SYNC STATUS: SYNCED
```

### Local Only
```text
PIPELINE: LOCAL_ONLY_COMPLETE
FEATURE ID: ART-FEAT-<MODULE>-###
TITLE: <title>
MODULE: <Module>
CLASSIFICATION: NEW_FEATURE / ENHANCEMENT
LOCAL STORAGE: STORED
LEDGER: UPDATED
AZURE: NOT_RUN
```
