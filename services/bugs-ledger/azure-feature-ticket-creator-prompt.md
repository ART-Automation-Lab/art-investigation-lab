# ART AZURE USER STORY TICKET HARNESS — HARNESS 02
VERSION: FEATURE BACKLOG AZURE SYNC

## PURPOSE

Take an existing canonical ART Feature record stored by Harness 01 and project
it into Azure DevOps as a developer-ready and AI-ready **User Story** work item.

Harness 02 is:
**AZURE SYNCHRONIZATION + VERIFICATION ONLY.**

Harness 02 NEVER:
- allocates Feature IDs
- invents unverified specifications
- creates Azure Features or Epics
- changes the canonical Module

---

## 1. INPUT

The user provides an existing canonical Feature ID (e.g. `ART-FEAT-AGENT-001`).

Harness 02 locates the record at:
`ART-Product-Validation/features/<MODULE>/<FEATURE-ID>__<slug>/<FEATURE-ID>.md`

---

## 2. PREFLIGHT VERIFICATION

Before creating any Azure mutation:
1. Verify the canonical Markdown file exists on disk.
2. Verify Azure credentials (`AZURE_DEVOPS_ORGANIZATION`, `AZURE_DEVOPS_PROJECT`, `AZURE_DEVOPS_PAT`).
3. Resolve the parent Azure Feature work item ID under Epic `Backlog Tickets` (#69099).
4. Perform WIQL query to check if a User Story with tag `ART:<FEATURE-ID>` already exists.

---

## 3. AZURE MUTATION CONTRACT

- **Parent Epic:** `Backlog Tickets` (#69099)
- **Work Item Type:** `User Story`
- **Fields:**
  - `System.Title`: `[<FEATURE-ID>] <Title>`
  - `System.Description`: Formatted HTML (Problem, Current Behavior, Proposed Behavior, Business Impact, User Experience, Guidance, Related Bugs).
  - `Microsoft.VSTS.Common.AcceptanceCriteria`: Formatted HTML list of criteria.
  - `System.Tags`: `ART:<FEATURE-ID>; <FEATURE-ID>; ART; Feature; <module>`
  - `System.History`: Audit note.
  - `Microsoft.VSTS.Common.ValueArea`: `Business`
  - `Relations`: Parent link (`System.LinkTypes.Hierarchy-Reverse`) to the resolved Feature work item.
- **Attachments:** All canonical evidence files attached with duplicate detection.

---

## 4. READBACK AND METADATA WRITEBACK

After creation/reconciliation:
1. Read back the work item from Azure DevOps via REST API.
2. Verify the work item ID, title, and parent link.
3. Update the canonical Markdown file on disk with:
   - `- **Azure Work Item ID:** #<id>`
   - `- **Azure Sync Status:** SYNCED`
4. Recompile `ART_FEATURE_BACKLOG_LEDGER.md`.
