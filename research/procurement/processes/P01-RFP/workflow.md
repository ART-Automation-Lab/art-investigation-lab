# Operational Workflow: RFP Requirement Review & Response Coordination (P01-RFP)

> **Process ID:** `P01-RFP`  
> **Process Name:** RFP Requirement Review & Response Coordination  
> **Process Owner:** Chiranjeevi  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)

---

## 1. As-Is Operational Workflow Topology

```text
[Tender Packet Ingestion] (PDF / Word / Scanned Document / Portal Download)
             │
             ▼
   [WF-P01-001: Initial Intake & Triage]
             │
             ▼
   [WF-P01-002: Clause Extraction & Parsing] ◄─── (High Human Effort / High Omission Risk)
             │
             ├───► [WF-P01-003a: Technical Routing] (Engineering / Solution Architecture)
             ├───► [WF-P01-003b: Security Routing] (CISO / Infosec / Compliance)
             ├───► [WF-P01-003c: Legal/Terms Routing] (Legal Counsel / Risk Management)
             └───► [WF-P01-003d: Commercial Routing] (Finance / Pricing / Executive)
             │
             ▼
   [WF-P01-004: Gap & Ambiguity Reconciliation]
             │
             ▼
   [WF-P01-005: Master Compliance Response Compilation]
             │
             ▼
   [WF-P01-006: Executive Gate & Final Submission]
             │
             ▼
   [Post-Award Contract Handoff] ───► [P02-SUPPLIER-DELIVERY]
```

---

## 2. To-Be ART Automation Topology (Proposed Architecture)

```text
┌────────────────────────────────────────────────────────┐
│ Input: Unstructured Tender Packet (PDF / Text / Doc)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Node 1: Document Layout & Structural Parser             │
│ - Chunking by formal section headings                   │
│ - Tabular extraction & paragraph boundary isolation    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Node 2: Forensic Clause Extraction Agent (LLM)         │
│ - Prompts: Ingestion prompt adhering to RFP-001 Schema  │
│ - Output Contract: JSON Array of requirement objects   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Node 3: Obligation & Functional Classifier Engine      │
│ - Obligation tagging: MANDATORY (must) / PREFERRED     │
│ - Domain routing: SECURITY, LEGAL, ENGINEERING, etc.   │
│ - Compliance default: UNKNOWN (Anti-hallucination)     │
│ - SME flag: SUGGESTED_NOT_CONFIRMED                    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Node 4: Traceability & Coverage Validator              │
│ - Line-by-line locator check (Section / Line numbers)  │
│ - Hallucination guard (zero ungrounded requirements)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Node 5: Human-in-the-Loop Proposal Manager Gate (HIL)  │
│ - Review flagged ambiguities (A1–A4 tiers)             │
│ - Affirm SME assignments prior to external routing     │
│ - Authorize master matrix export                       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Output: Auditable Compliance Matrix & Route Notifications
└────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Step Specifications & Data Contracts

### `WF-P01-001`: Tender Intake & Registration
- **Trigger:** Formal receipt of tender documents via procurement portal, public notice, or client email.
- **Operator:** Proposal Coordinator / Commercial Lead.
- **Inputs:** Tender metadata (Issuing Agency, Tender Number, Submission Deadline, Clarification Window Cutoff).
- **Activities:** Register tender in tracking repository; verify document completeness (check for missing schedules, exhibits, or price sheets).
- **Artifacts:** Master bid dossier, timestamped source archive.

### `WF-P01-002`: Structural Decomposition & Clause Extraction
- **Operator:** Forensic Extraction Agent (ART) supervised by Proposal Engineer.
- **Inputs:** Cleaned tender text stream.
- **Contract Schema (JSON Object per requirement):**
  ```json
  {
    "requirement_id": "REQ-001",
    "section_title": "3.1 Data Residency and Sovereign Hosting",
    "source_clause": "The platform must host all production data within EU borders.",
    "obligation_type": "MANDATORY",
    "suggested_sme_area": "SECURITY",
    "compliance_status": "UNKNOWN",
    "source_page": 12,
    "source_paragraph": 4
  }
  ```
- **Decision Rules:**
  - If text contains `must`, `shall`, `required`, `mandatory` $\rightarrow$ `MANDATORY`.
  - If text contains `should`, `preferred`, `optional`, `may` $\rightarrow$ `PREFERRED`.
  - If obligation modal verb is ambiguous or conditional $\rightarrow$ Flag as `AMBIGUOUS` with ambiguity tier `A2`.

### `WF-P01-003`: Functional SME Routing Engine
- **Operator:** Automated Router with HIL Confirmation.
- **Routing Rules:**
  - Technical architecture, API integrations, throughput $\rightarrow$ **Engineering**.
  - Encryption, access control, certifications (SOC 2, ISO 27001) $\rightarrow$ **Security/CISO**.
  - Indemnity, governing law, IP ownership, liability caps $\rightarrow$ **Legal Counsel**.
  - Unit pricing, volume tiers, payment terms $\rightarrow$ **Commercial Finance**.
- **Safety Boundary:** All SME assignments must be stamped `SUGGESTED_NOT_CONFIRMED` until explicitly confirmed by the human proposal manager.

### `WF-P01-004`: Clarification Cycle & Addendum Processing
- **Operator:** Proposal Manager.
- **Activities:** If unresolvable contradictions appear in tender requirements (Ambiguity tier `A3`), compile formal inquiries for submission to the buyer during the clarification window.
- **Addendum Handling:** When addenda are published, re-run differential extraction to identify amended clause text and update requirements in-flight.

### `WF-P01-005`: Master Compliance Response Matrix Assembly
- **Operator:** ART Response Aggregator.
- **Outputs:** Tabular matrix linking requirement text, section locator, compliance declaration (`COMPLIANT`, `COMPLIANT_WITH_EXCEPTION`, `NON_COMPLIANT`), SME response text, and supporting artifact link.

### `WF-P01-006`: Final Governance Gate & Sign-Off
- **Operators:** Executive Sponsor, General Counsel, Finance Director.
- **Activities:** Mandatory human review before bid submission. Validate zero unassigned mandatory clauses and zero unresolved legal exceptions.

---

## 4. Cross-Process Hand-Off Boundaries

- **Downstream to P02 (Supplier Delivery):**
  Upon commercial award, all contractual milestones, delivery lead-time commitments, and SLA penalty terms transition to [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/) to govern Purchase Order fulfillment and delay escalation.
- **Downstream to P04 (Invoice Exceptions):**
  Agreed milestone payment schedules, unit pricing rate cards, and billing requirements transition to [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/) to establish baseline 3-way match rules.

---

## 5. References

- Investigation Brief: [`investigation.md`](./investigation.md)
- Evidence Log: [`evidence.md`](./evidence.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
- Execution Records: [`executions/`](./executions/)
