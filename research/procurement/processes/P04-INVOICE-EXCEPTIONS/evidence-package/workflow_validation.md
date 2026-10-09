# Workflow Validation & Stage Audit: P04 Invoice Discrepancy Resolution

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Process Owner:** Ashwin (`ashwinash19`)  
> **Source Workflow:** [`workflow.md`](../workflow.md)  
> **Investigation Brief:** [`investigation.md`](../investigation.md)  
> **Creation Date:** 2026-10-09  
> **Validation Status:** Stage Architecture Audited; Operational Gaps Identified

---

## 1. Operational Workflow Stage-by-Stage Audit

```text
[Vendor Invoice] 
      │
      ▼
[WF-P04-001: Capture & Extraction] ────► CAPABILITY GAP (No OCR tool)
      │
      ▼
[WF-P04-002: 3-Way Match] ─────────────► READY (Deterministic math on PO, PR, PI)
      │
      ▼
[WF-P04-003: Categorization] ──────────► READY (Price / Qty / Freight / Tax rules)
      │
      ▼
[WF-P04-004: Triage & Routing] ────────► READY (P01 Buyer vs P02 Dock routing)
      │
      ▼
[WF-P04-005: Dispute Settlement] ──────► PARTIAL (Drafting only; no memo tools)
      │
      ▼
[WF-P04-006: Block Removal / Post] ────► BOUNDARY CONFLICT (Treasury handoff)
```

---

## 2. Stage-by-Stage Detailed Audit

### `WF-P04-001`: Invoice Capture & Header/Line Extraction
* **Purpose:** Ingest vendor invoices (PDF, XML, EDI) and extract structured header and line-item data.
* **Required Inputs:** Invoice document or image.
* **Supporting ART Tools:** **None available** in `erpnext_art` provider.
* **Actual Evidence:** Dependency audit of workspace confirms 0 OCR engines or document parsers exist.
* **Failure Condition:** Ingesting unstructured or scanned PDFs fails immediately.
* **Operational Workaround:** Invoices must enter as pre-structured ERPNext `Purchase Invoice` documents.
* **Validation Status:** **CAPABILITY GAP (UNSUPPORTED)**

---

### `WF-P04-002`: Automated 3-Way Match Evaluation
* **Purpose:** Compare line items, quantities, and rates across Purchase Order, Purchase Receipt, and Purchase Invoice.
* **Required Inputs:** `Purchase Order` JSON, `Purchase Receipt` JSON, `Purchase Invoice` JSON.
* **Supporting ART Tools:** `erpnext_get_purchase_order`, `erpnext_get_purchase_receipt`, `erpnext_get_purchase_invoice`.
* **Actual Evidence:** All 3 read tools are published and tested clean via HTTP 200 list responses.
* **Validation Rules:**
  1. $Qty_{billed} \le Qty_{received} \le Qty_{ordered}$
  2. $Rate_{billed} = Rate_{ordered}$
  3. $Amount_{billed} = Qty_{billed} \times Rate_{billed} + Tax + Freight$
* **Failure Condition:** Unretrievable PO/PR or mismatched units of measure.
* **Validation Status:** **READY FOR EMPIRICAL TESTING**

---

### `WF-P04-003`: Discrepancy Categorization & Hold
* **Purpose:** Isolate variance root causes and apply financial categorization:
  * `PRICE_VARIANCE`: Invoiced rate exceeds PO rate.
  * `QUANTITY_VARIANCE`: Invoiced quantity exceeds physical received quantity on receipt.
  * `UNAUTHORIZED_FEES`: Disputed freight, demurrage, or handling not authorized on PO.
  * `TAX_DISCREPANCY`: Incorrect GST/VAT rate or tax calculation discrepancy.
* **Supporting Tools:** Agent prompt deterministic logic.
* **Actual Evidence:** Categorization schema documented in `workflow.md`.
* **Validation Status:** **DESIGN VERIFIED**

---

### `WF-P04-004`: Root-Cause Triage & Cross-Team Routing
* **Purpose:** Route discrepancy dossiers to appropriate functional teams:
  * Unit Price Variance $\rightarrow$ Procurement Buyer (`P01-RFP` handoff).
  * Quantity Variance $\rightarrow$ Receiving Dock / Logistics (`P02-SUPPLIER-DELIVERY` handoff).
  * Freight / Extra Surcharges $\rightarrow$ Sourcing & Logistics.
* **Supporting Tools:** Agent reasoning & evidence synthesis.
* **Validation Status:** **DESIGN VERIFIED**

---

### `WF-P04-005`: Dispute Settlement & Commercial Action
* **Purpose:** Draft formal dispute inquiry, recommend settlement path (Credit Note, Debit Memo, PO Revision, Rejection).
* **Supporting Tools:** Agent dossier generation.
* **Boundary Guardrail:** The agent can only **recommend and draft** communications; it has zero authorization to post financial adjustments or create credit notes autonomously.
* **Validation Status:** **PARTIAL (HUMAN-IN-THE-LOOP REQUIRED)**

---

### `WF-P04-006`: Block Removal & Payment Release
* **Purpose:** Remove payment block and schedule payment run.
* **CRITICAL PROCESS BOUNDARY CONFLICT:**
  * [`workflow.md`](../workflow.md) includes payment release under Stage 6.
  * [`investigation.md`](../investigation.md) explicitly states: *"Treasury cash forecasting, payment execution, and bank disbursement (treasury handoff) are Out-of-Scope."*
  * Master Prompt Section 2.1 states: *"It must not autonomously release payments, disburse funds, approve financial adjustments."*
* **Resolution Requirement:** `WF-P04-006` must be formally classified as a **Controlled Handoff to Treasury / AP Supervisor Run**, terminating autonomous agent activity at stage `WF-P04-005`.
* **Validation Status:** **CONFLICT FLAGGED — REQUIRES OWNER CONFIRMATION**
