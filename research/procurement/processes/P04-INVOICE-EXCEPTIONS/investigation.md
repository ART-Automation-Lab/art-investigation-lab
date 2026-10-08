# Investigation: Invoice Discrepancy Resolution (P04-INVOICE-EXCEPTIONS)

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Process Owner:** Ashwin (Process Owner)  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)  
> **Master Prompt:** [`../../MASTER_PROMPT.md`](../../MASTER_PROMPT.md)  
> **Current Epistemic Level:** Baseline Initialized (`E0` hypotheses, unverified)

---

## 1. Process Scope & Operational Boundary

### In-Scope:
- Multi-source invoice ingestion (EDI 810, XML e-invoices, PDF attachments, scanned paper).
- Automated 3-way matching across Purchase Order (PO), Goods Receipt Note (GRN), and Supplier Invoice.
- Identification and categorization of match discrepancies:
  - Unit price variance (PO price vs. invoiced price).
  - Quantity discrepancy (delivered quantity vs. invoiced quantity).
  - Unapproved incidental charges (freight, fuel surcharges, handling fees, pallet fees).
  - Tax code, GST/VAT, and line-item calculation errors.
- Cross-departmental dispute workflows involving Accounts Payable (AP), Procurement Category Buyers, Receiving Dock, and Supplier AR teams.
- Credit note generation, debit memo issuance, or invoice rejection and payment release.

### Out-of-Scope (Handoffs):
- Sourcing contract price terms and commercial discounts (governed in [`../P01-RFP/`](../P01-RFP/)).
- Physical carrier freight tracking and in-transit monitoring (governed in [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/)).
- Treasury cash forecasting, payment execution, and bank disbursement (treasury handoff).

---

## 2. Core Investigation Questions

1. **Exception Rate Reality:** What is the actual, audited percentage of enterprise supplier invoices that fail automated 3-way match, and what are the top root causes?
2. **Resolution Cost per Invoice:** What is the average fully-loaded organizational cost (in human hours and administrative overhead) to manually resolve an AP exception versus a straight-through processed invoice?
3. **Incumbent Limitations:** Why do existing AP automation tools (Coupa Pay, Basware, SAP Ariba Invoice Management, Tipalti) struggle to resolve non-PO freight surcharges and partial quantity disputes autonomously?
4. **Dispute Resolution Latency:** How many business days does an invoice spend suspended in AP exception holds, and how often does this result in missed early-payment discounts or vendor credit holds?

---

## 3. Incumbent Software Landscape & Automation Deficits

| Software Category | Typical Vendors | Current Automation Capabilities | Critical Failure Points & Manual Deficits |
|---|---|---|---|
| **AP Automation Suites** | Basware, Coupa Invoicing, SAP Ariba Invoice Pro | Optical character recognition (OCR), configurable tolerance matching, basic automated approval routing. | Brittle OCR error rates on non-standard PDF formats; cannot perform contextual reasoning on ambiguous charges (e.g., unexpected demurrage or emergency freight); dumps exceptions into human queues. |
| **ERP Financials (AP)** | SAP S/4HANA (FI-AP), Oracle Financials Cloud | Rigid 3-way matching logic, payment block flags, automated debit memo generation. | Pure pass/fail logic; if variance exceeds $0.05 or 1%, invoice is blocked with zero context; buyers must manually investigate physical receiving records and email threads. |
| **e-Invoicing & Compliance Networks** | Tungsten Network, Tradeshift, Peppol Access Points | Structured electronic invoice exchange, statutory tax validation. | Solves transmission format issues, but does not prevent business logic disputes (e.g., supplier billed pre-amendment price). |

---

## 4. Operational Failure Modes & High-Consequence Risks

- **Duplicate or Erroneous Payments:** Weak exception auditing allows duplicate billings or unauthorized supplier price hikes to slip through, causing direct cash loss.
- **Supplier Credit Hold:** Protracted disputes leave vendor invoices unpaid past payment terms, causing the supplier to freeze future deliveries and disrupting operations.
- **Lost Early-Payment Discounts:** Lengthy AP resolution cycles forfeit lucrative 2/10 net 30 payment discounts, costing large enterprises millions annually.

---

## 5. Investigation Next Steps & Artifact References

- Evidence Log: [`evidence.md`](./evidence.md)
- Operational Workflow Map: [`workflow.md`](./workflow.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
- Central Ambiguity Log: [`../../AMBIGUITIES.md`](../../AMBIGUITIES.md)
