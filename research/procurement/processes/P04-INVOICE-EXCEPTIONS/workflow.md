# Operational Workflow: Invoice Discrepancy Resolution (P04-INVOICE-EXCEPTIONS)

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Process Owner:** Ashwin  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)

---

## 1. As-Is Operational Workflow Topology

```text
[Supplier Invoice Received] (EDI / PDF / Portal / Mail)
             │
             ▼
   [WF-P04-001: Invoice Capture & Header/Line Extraction]
             │
             ▼
   [WF-P04-002: Automated 3-Way Match Evaluation]
   (Compare Invoice vs. PO vs. Goods Receipt Note)
             │
       ┌─────┴────────────────────────┐
       ▼                              ▼
  [Match Passed]            [Discrepancy Detected]
       │                              │
       │                              ▼
       │               [WF-P04-003: Discrepancy Categorization]
       │               (Price Variance / Qty Mismatch / Extra Freight / Tax)
       │                              │
       │                              ▼
       │               [WF-P04-004: Root Cause Triage & Cross-Team Routing]
       │               ├── Price Issue ──► Buyer / Procurement (P01)
       │               ├── Qty Issue   ──► Receiving Dock / Logistics (P02)
       │               └── Freight/Fee ──► Logistics & Sourcing
       │                              │
       │                              ▼
       │               [WF-P04-005: Dispute Settlement & Commercial Action]
       │               ├── Credit Note / Debit Memo
       │               ├── PO Revision Approval
       │               └── Rejection back to Vendor
       │                              │
       ▼                              ▼
   [WF-P04-006: Payment Release & General Ledger Posting]
```

---

## 2. Detailed Step Specifications

### `WF-P04-001`: Invoice Capture & Extraction
- **Trigger:** Invoice arrives in AP inbox or EDI subsystem.
- **System / Operator:** Optical Character Recognition (OCR) Engine / AP Scanning Clerk.
- **Activities:** Extract header data (vendor name, invoice number, tax ID, total amount) and line items (part number, quantity, unit price, extended price).

### `WF-P04-002`: Automated 3-Way Matching Engine
- **System:** ERP AP Module (e.g., SAP MIRO, Oracle Payables).
- **Activities:** Automatically match invoice lines against corresponding Purchase Order lines and Goods Receipt Notes (GRN).
- **Success:** If within defined financial tolerance limits (e.g., $2.00 or 0.5%), post invoice automatically to GL for payment.

### `WF-P04-003`: Discrepancy Classification & Blocking
- **System / Operator:** AP System / Exception Clerk.
- **Activities:** If match fails, place payment block on invoice. Classify discrepancy:
  - `PRICE_VARIANCE`: Invoiced price higher than PO unit price.
  - `QUANTITY_VARIANCE`: Invoiced quantity exceeds physical received quantity on dock.
  - `UNAUTHORIZED_FEES`: Fuel surcharges, handling fees, or freight not on PO.
  - `TAX_DISCREPANCY`: Incorrect tax rate or missing exemption certificate.

### `WF-P04-004`: Root-Cause Triage & Cross-Functional Routing
- **Operator:** AP Exception Specialist.
- **Activities:**
  - Route price variances to responsible buyer to determine if an unrecorded amendment was agreed.
  - Route quantity variances to warehouse receiving dock to check if goods arrived damaged or are pending inspection.

### `WF-P04-005`: Dispute Resolution & Financial Settlement
- **Operators:** Buyer, AP Manager, Supplier AR Contact.
- **Resolution Paths:**
  1. Vendor issues Credit Note for difference.
  2. Buyer executes retroactive PO line change order (if price increase was contractually legitimate).
  3. AP issues short-payment with formal debit memo explanation.
  4. Full invoice rejection and request for re-billing.

### `WF-P04-006`: Block Removal & Payment Release
- **System / Operator:** AP Supervisor / Payment Scheduling Run.
- **Activities:** Remove payment block, schedule payment in according with net terms (e.g., Net 30, Net 60), post realized discount/gain to GL.

---

## 3. Cross-Process Boundaries & Dependencies

- **Upstream from P01 (RFP):** Relies on baseline contracted price schedules, volume discounts, and payment terms negotiated in [`../P01-RFP/`](../P01-RFP/).
- **Upstream from P02 (Supplier Delivery):** Depends on accurate Goods Receipt Notes (GRN) and delivery timestamps created upon physical arrival from [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/).
- **Coupled with P03 (Replenishment):** Reorder quantities and supplier lead-time emergency charges directly influence invoice line items generated via [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/).

---

## 4. References & Documentation

- Investigation Brief: [`investigation.md`](./investigation.md)
- Evidence Log: [`evidence.md`](./evidence.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
