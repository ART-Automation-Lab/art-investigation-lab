# ART FEATURE INTAKE & STORAGE HARNESS — HARNESS 01
VERSION: CANONICAL FEATURE STORAGE

## PURPOSE

Convert raw user requests, improvement proposals, and design ideas into structured,
canonical ART feature records stored under the correct ART module directory.

This harness is responsible for:
1. Structuring the feature request into canonical format.
2. Allocating or preserving the durable Feature ID (`ART-FEAT-<MODULE>-###`).
3. Detecting near-duplicates and existing requests.
4. Storing the canonical Markdown record under `ART-Product-Validation/features/<MODULE>/<FEATURE-ID>__<slug>/`.
5. Storing supplied evidence (mockups, screenshots, logs).
6. Updating the feature backlog ledger (`ART_FEATURE_BACKLOG_LEDGER.md`).
7. Checking readiness for Azure DevOps synchronization.

This harness is:
**STORAGE + STRUCTURING + LOCAL MODULE ROUTING ONLY.**
NEVER create or modify Azure DevOps work items directly from Harness 01.

---

## 1. INPUT

The user may provide:
- Feature title or raw description
- Problem or opportunity description
- Current behavior vs proposed behavior
- Business impact and user experience
- Implementation guidance
- Acceptance criteria
- Module or component
- Related Bug IDs
- Evidence files (screenshots, mockups)
- Existing Feature ID (for updates)

---

## 2. CANONICAL MODULE DIRECTORY MAPPING

All features must belong to one canonical ART Module folder:
- `Agent Lab` → `features/Agent Lab/`
- `Orchestrator` → `features/Orchestrator/`
- `Tool Builder` → `features/Tool Builder/`
- `MCP Servers` → `features/MCP Servers/`
- `Triggers` → `features/Triggers/`
- `Credential Manager` → `features/Credential Manager/`
- `Serverless Functions` → `features/Serverless Functions/`
- `Governance` → `features/Governance/`
- `Human-in-the-Loop / Approvals` → `features/Human-in-the-Loop - Approvals/`
- `Live Connect` → `features/Live Connect/`
- `ART Development Kit (ADK)` → `features/ART Deployment Kit (ADK)/`
- `Agent X` → `features/Agent X/`

---

## 3. CANONICAL MARKDOWN SPECIFICATION

Each feature record must contain:

```markdown
# <FEATURE-ID> — <Feature Title>

- **Module:** <Canonical Module>
- **Classification:** <NEW_FEATURE / ENHANCEMENT>
- **Status:** <PROPOSED / ACCEPTED / IN_PROGRESS / IMPLEMENTED / REJECTED / BLOCKED>
- **Priority:** <P1 / P2 / P3 / P4>
- **Azure Work Item ID:** <#ID or None>
- **Azure Sync Status:** <NOT_SYNCED / SYNCED / FAILED>

## Problem / Opportunity

<Detailed statement of the unmet user need, limitation, or improvement opportunity>

## Current Behavior

<How the product behaves today without this feature>

## Proposed Behavior

<Specific, concrete description of the requested capability or workflow>

## Business Impact

<Efficiency gains, capabilities enabled, customer value>

## User Experience

<UI interaction, navigation, workflow changes>

## Acceptance Criteria

1. <Criterion 1>
2. <Criterion 2>

## Implementation Guidance

<Architectural notes, files to inspect, APIs to extend>

## Related Bugs / Dependencies

- <Related Bug ID or Work Item>

## Evidence and Provenance

- **Provenance:** HUMAN_SUPPLIED
- **Created At:** <ISO Timestamp>
- **Updated At:** <ISO Timestamp>
- **Evidence Files:**
  - `<filename>` (SHA-256: `<hash>`)
```

---

## 4. DUPLICATE AND BUG COLLISION GUARDS

1. **Duplicate Guard:** Checks existing feature titles and problem statements. If similarity >= 65%, flags as near-duplicate and requires explicit `allow_update` confirmation.
2. **Defect Disambiguation Guard:** Checks if the request describes a software crash, regression, or failure of an existing advertised capability. Flags advisory warning if the request should properly be filed as a Bug.
