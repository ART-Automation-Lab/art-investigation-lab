# AIL Investigation Brief Contract v1

## 1. WHAT IT IS
The AIL Investigation Brief Contract v1 is the canonical specification defining the exact structure, vocabulary, and semantic meaning required for an ART Opportunities Intelligence (AOI) `walkthrough.md` document. It is a strict data contract disguised as Markdown.

## 2. WHY IT EXISTS
To preserve research integrity, AIL must act solely as a validator, normalizer, and presenter of research. The Art Investigation Lab (AIL) UI is not allowed to guess or infer research meaning from arbitrary prose (e.g., guessing what a final decision is based on a paragraph of text). This contract explicitly dictates where and how AOI must declare its findings so AIL can reliably extract them without assumptions.

## 3. WHO PRODUCES IT
**AOI (Art Opportunities Intelligence)** produces the Investigation Brief (`walkthrough.md`). AOI owns the research, the interpretation of evidence, the formulation of hypotheses, the reasoning logic, and the final decision. 

## 4. WHO CONSUMES IT
**AIL (Art Investigation Lab)** consumes the Brief. AIL owns the validation of the contract, the normalization of the text into the Canonical Investigation Model, and the presentation of that model in the UI.

## 5. WHAT AIL MUST NEVER INFER
- AIL must NEVER infer a research question from a generic paragraph.
- AIL must NEVER silently convert an INFERENCE into a FACT or an UNKNOWN into a CLAIM.
- AIL must NEVER infer the final decision; AOI must explicitly declare it.
- AIL must NEVER manufacture missing data to fill UI fields.

## 6. REQUIRED VS. OPTIONAL VS. INVALID
- **REQUIRED**: A field or section that must exist for the brief to be valid (e.g., Identity, Final Decision). Missing required fields produce an `INVALID` validation error.
- **OPTIONAL**: A field that adds richness but is not strictly necessary (e.g., Reusable Intelligence). If omitted, AIL gracefully maps it to `NOT PROVIDED`.
- **UNKNOWN**: A research state where AOI explicitly declares that an answer is unknown. This is a valid research outcome, distinct from `NOT PROVIDED`.
- **INVALID**: A structural failure (e.g., a missing required field, an unrecognized status string, or a broken reference).

---

## 7. SEMANTIC SECTIONS

### 1. IDENTITY (Required)
Defines the metadata of the investigation.
- **investigationId**: Required. (e.g., `AOI-SNOW-OPP-002`)
- **company**: Required. The target company.
- **opportunity**: Required. The name/title of the opportunity.
- **investigationType**: Optional. The stages of the investigation.
- **researchStatus**: Required. The final status of the research.
- **decision**: Required. (e.g., `KILL`, `PURSUE`).
- **sourceResearchFiles**: Required. Links to source checkpoints.

### 2. RESEARCH QUESTION (Required)
- **primaryQuestion**: The core question being investigated.
- **whyInvestigationExists**: The business/technical rationale driving the investigation.

### 3. INITIAL HYPOTHESIS (Required)
- **hypothesis**: The starting hypothesis statement.
- **status**: Controlled state (e.g., `UNVALIDATED`, `ACTIVE`, `SUPPORTED`, `WEAKENED`, `KILLED`, `UNKNOWN`).
- **rationale**: Why this hypothesis was formed.

### 4. INVESTIGATION PROGRESSION (Required)
An unlimited, variable-length sequence of Checkpoints representing the timeline.
Each Checkpoint must provide:
- **checkpointId**: Unique identifier (e.g., `OPP-002-01`).
- **question**: What was being tested.
- **whatChanged**: The finding or progression step.
- **evidence**: The specific evidence triggering the change.
- **resultingState**: The research status at the end of the checkpoint.
- **decision**: The micro-decision made.
- **provenance**: Source file reference.

### 5–8. EPISTEMIC OBJECTS (Required)
Must remain strictly separated. Never silently transform one into another.
- **EVIDENCE**: 
  - `id`, `statement`, `classification` (e.g., DIRECT EVIDENCE), `source`, `provenance`.
- **CLAIM**: 
  - `id`, `statement`, `evidenceRefs` (must point to EVIDENCE), `provenance`.
- **INFERENCE**: 
  - `id`, `statement`, `basisRefs`, `provenance`.
- **HYPOTHESIS**: 
  - `id`, `statement`, `status`, `basisRefs`, `provenance`.

### 9. CONTRADICTIONS / FALSIFICATIONS (Required)
Items that were explicitly tested and rejected.
- `id`, `targetRef`, `whatWasTested`, `evidence`, `outcome` (Controlled: `KILLED`, `WEAKENED`, `UNRESOLVED`, `SURVIVED`), `reason`, `provenance`.

### 10. SURVIVING FINDINGS (Optional)
Findings that remain valid. Must be explicitly declared, not just "not killed".
- `id`, `statement`, `supportingRefs`, `confidence/status`, `provenance`.

### 11. FINAL DECISION (Required)
- **decision**: The explicit AOI decision.
- **decisionReason**: Why the decision was made.
- **supportingRefs**: Links to evidence/findings.
- **remainingUnknowns**: What remains unanswered.
- **decisionStatus**: Controlled status.

### 12. REUSABLE INTELLIGENCE (Optional)
Knowledge useful beyond this specific opportunity.
- `id`, `statement`, `applicability`, `sourceRefs`, `provenance`.

### 13. RESEARCH LIMITATIONS (Required)
Explicit capture of validation debt.
- `unknowns`, `evidenceLimitations`, `unverifiedAssumptions`, `unresolvedQuestions`, `validationDebt`.

### 14. TRACEABILITY (Required)
Every major object must trace back to the source file, section, and exact location.

---

## 8. CONTROLLED STATUS VOCABULARY
Arbitrary status strings are prohibited. If an unrecognized string is used, AIL will throw a validation warning and will NOT silently normalize it into a valid status.
**Allowed Core Statuses**: `UNKNOWN`, `UNVERIFIED`, `PENDING`, `ACTIVE`, `PASSED`, `FAILED`, `BLOCKED`, `SURVIVED`, `KILLED`, `WEAKENED`, `SUPPORTED`, `UNRESOLVED`.

## 9. HOW VALIDATION WORKS
AIL validates the contract by parsing the Markdown AST. It checks for:
- Missing required sections or fields.
- Unrecognized status values.
- Duplicate IDs or broken references (e.g., a Claim pointing to missing Evidence).
- Epistemic violations (e.g., an Inference masquerading as Evidence).
Validation produces machine-readable issues:
`INVALID | Field: finalDecision | Reason: required field missing | Source: walkthrough.md`

## 10. HOW PROVENANCE WORKS
Every extracted semantic object (Checkpoint, Evidence, Claim) is tagged with a `Provenance` object containing:
`document` (e.g., walkthrough), `sourcePath`, `section` (heading), `sourceIdentifier`, `lineStart`, `lineEnd`.
This guarantees that AIL can always trace UI data back to the exact AOI Markdown coordinate.

## 11. HOW SCALABILITY WORKS
The contract uses repeating structures (Markdown tables, lists) for arrays (Checkpoints, Evidence). 
- If research has 3 checkpoints or 100 checkpoints, the parser iterates the table rows dynamically.
- Missing optional fields seamlessly map to `NOT PROVIDED` without breaking the parser.
- Changing opportunity titles or target companies requires zero AIL code changes, as the canonical model is agnostic to the research content.

---

## 12. CANONICAL MODEL CONCEPT
The AIL Canonical Model is the normalized TypeScript interface that consumes this contract.
```typescript
interface CanonicalInvestigation {
  identity: IdentityModel;
  researchQuestion: QuestionModel;
  initialHypothesis: HypothesisModel;
  progression: CheckpointModel[];
  evidence: EvidenceModel[];
  claims: ClaimModel[];
  inferences: InferenceModel[];
  hypotheses: HypothesisModel[];
  falsifications: FalsificationModel[];
  findings: FindingModel[];
  decision: DecisionModel;
  intelligence: IntelligenceModel[];
  limitations: LimitationsModel;
}
```

---

## 13. CONTRACT EXAMPLE (SYNTHETIC)

**AOI Markdown (Input):**
```markdown
## Identity
| Field | Value |
|---|---|
| Company | Acme Corp |
| Opportunity | Automated Widget Generation |
| AOI decision | PURSUE |

## Epistemic Objects
- **Evidence:** Acme API rate limits are 10k/sec. (Source: Acme Docs)
- **Claim:** The API can support our projected 5k/sec volume.
```

**Contract Meaning (Validation):**
- Extracts Identity table. Validates `Company`, `Opportunity`, `decision`.
- Extracts Epistemic list. Validates `Evidence` and `Claim` isolation. Ensures Claim is not labeled as Evidence.

**Normalized Object (Output):**
```json
{
  "identity": {
    "company": "Acme Corp",
    "opportunity": "Automated Widget Generation",
    "decision": "PURSUE"
  },
  "evidence": [{ "id": "ev-1", "statement": "Acme API rate limits are 10k/sec." }],
  "claims": [{ "id": "cl-1", "statement": "The API can support our projected 5k/sec volume." }]
}
```
