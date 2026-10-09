# Evidence Inventory: P04 Invoice Discrepancy Resolution

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Process Owner:** Ashwin (`ashwinash19`)  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../../RESEARCH_STANDARD.md)  
> **Master Evidence Register:** [`../../EVIDENCE_REGISTER.md`](../../../EVIDENCE_REGISTER.md)  
> **Creation Date:** 2026-10-09  
> **Epistemic Principle:** Zero fabrication. Rigorous separation of hypothesis (`E0`), public documentation (`E1`), industry pain (`E2`), practitioner testimony (`E3`), and direct empirical operational validation (`E4`).

---

## 1. Epistemic Classification Framework

All evidence items recorded in this inventory adhere to the 5-tier taxonomy established in [`RESEARCH_STANDARD.md`](../../../RESEARCH_STANDARD.md):

* **`E0` — Hypothesis:** Speculative or unverified working assumption.
* **`E1` — Public Process Documentation:** Verified against official vendor documentation or statutory standard.
* **`E2` — Documented Industry Pain Point:** Verifiable benchmark, audit survey, or published operational study.
* **`E3` — Practitioner Testimony:** Direct testimony from enterprise AP or procurement operators.
* **`E4` — Direct Operational Validation:** Direct operational execution, verified API payload, or audited system record.

---

## 2. P04 Master Evidence Register

| Evidence ID | Level | Category | Source / Provenance | Exact Observed Data / Excerpt | Supported Finding / Claim | Status |
|---|---|---|---|---|---|---|
| `EVD-P04-001` | `E0` | Operational | Internal Workspace Architecture | *"A significant majority of enterprise AP exception cycle times are spent in inter-departmental communication between Accounts Payable and Procurement buyers."* | `CLM-P04-001` | `HYPOTHESIS_PENDING_STUDY` |
| `EVD-P04-002` | `E4` | Legal Entity | Live ART Tool Execution: `erpnext_find_docs_list` | Execution in 75.9 ms: `{"message": [{"name": "Aiotrix"}]}` | Confirms legal company entity in live ERPNext is exactly `"Aiotrix"`. | `VERIFIED` |
| `EVD-P04-003` | `E4` | Master Data | Live ART Tool Execution: `erpnext_list_supplier` | Execution in 160.0 ms: `{"data": []}` | Confirms 0 active Supplier records exist post demo cleanup. | `VERIFIED` |
| `EVD-P04-004` | `E4` | Master Data | Live ART Tool Execution: `erpnext_find_docs_list` | Execution in 110.1 ms: `{"message": []}` | Confirms 0 active Item records exist post demo cleanup. | `VERIFIED` |
| `EVD-P04-005` | `E4` | Transactions | Live ART Tool Execution: `erpnext_list_purchase_order` | Execution in 96.6 ms: `{"data": []}` | Confirms Purchase Order transaction table is empty. | `VERIFIED` |
| `EVD-P04-006` | `E4` | Transactions | Live ART Tool Execution: `erpnext_list_purchase_receipt`| Execution in 109.7 ms: `{"data": []}` | Confirms Purchase Receipt transaction table is empty. | `VERIFIED` |
| `EVD-P04-007` | `E4` | Transactions | Live ART Tool Execution: `erpnext_list_purchase_invoice`| Execution in 156.6 ms: `{"data": []}` | Confirms Purchase Invoice transaction table is empty. | `VERIFIED` |
| `EVD-P04-008` | `E4` | Tool Defect | Provider Export: `art-tool-provider-erpnext_art.json` | Body mapping: `{"kind": "json", "value": {"description": "{params.data}"}}` | Proves `erpnext_create_docs_list` wraps payload into `description` with ToDo schema. | `VERIFIED` |
| `EVD-P04-009` | `E4` | Tool Defect | Provider Export: `art-tool-provider-erpnext_art.json` | Hardcoded field: `"supplier": "MediSupply Healthcare Pvt Ltd"` | Proves `create_purchase_receipt` ignores PO supplier and hardcodes fixed entity. | `VERIFIED` |
| `EVD-P04-010` | `E4` | Architecture | Workspace Dependency Audit | Zero OCR/PDF packages in `package.json`, zero ingestion tools in provider | Proves P04 has no autonomous PDF extraction capability; requires ERPNext records. | `VERIFIED` |
| `EVD-P04-011` | `E4` | Historical | Historical Execution Log: `erpnext_get_purchase_order` | `PUR-ORD-2026-00001` returned PO: Supplier `Zuckerman Security Ltd.`, 100 units @ 400 INR | Proves PO retrieval tool endpoint functions when record exists. | `HISTORICAL_VERIFIED` |
| `EVD-P04-012` | `E4` | Historical | Historical Execution Log: `erpnext_get_purchase_receipt`| Query `PUR-ORD-2026-00001` returned HTTP 404 `DoesNotExistError` | Proves DocType mismatch handling; PR endpoint rejects PO identifier cleanly. | `HISTORICAL_VERIFIED` |
| `EVD-P04-013` | `E4` | Live Execution | ART Provider Execution: 11 Unique Tools | 12 tests executed via connector `erpnext_p04_readonly`: 100% PASS rate across all 11 unique tools | Proves core read/retrieval integration layer is fully operational. | `VERIFIED` |
| `EVD-P04-014` | `E4` | Master Data | Live Tool Execution: `erpnext_list_supplier` | Query returned `P02 Test Supplier` & `P04-Test-Coastal Industrial Components` | Proves active suppliers exist in ERPNext instance for procurement workflows. | `VERIFIED` |
| `EVD-P04-015` | `E4` | Master Data | Live Tool Execution: `erpnext_find_docs_list(Item)` | Query returned `P02-TEST-ITEM-001` & `P03-TEST-ITEM-001` | Proves active purchasable items exist in ERPNext instance. | `VERIFIED` |
| `EVD-P04-016` | `E4` | Transaction Data | Live Tool Execution: `erpnext_get_purchase_order` | PO `PUR-ORD-2026-00011` retrieved: `P02 Test Supplier`, 1 Nos @ ₹1.00 (`docstatus=1`) | Proves live submitted PO available for 3-way match validation. | `VERIFIED` |
| `EVD-P04-017` | `E4` | Transaction Data | Live Tool Execution: `erpnext_get_purchase_receipt`| PR `PR-26-00001` retrieved in 111.3 ms: 1 received, 0 rejected, Rate ₹1.00 (`docstatus=1`) | Proves live submitted receiving record available for 3-way match. | `VERIFIED` |
| `EVD-P04-018` | `E4` | Transaction Data | Live Tool Execution: `erpnext_get_purchase_invoice`| PI `PINV-26-00007` retrieved in 77.1 ms: submitted (`docstatus=1`) | Proves live submitted invoice available for 3-way match comparison. | `VERIFIED` |

---

## 3. Epistemic Traceability and Cross-References

- **Upstream Process Handoffs:**  
  * Sourcing price baseline: Handed off from [`../P01-RFP/`](../../P01-RFP/).
  * Goods delivery timestamps & ASNs: Handed off from [`../P02-SUPPLIER-DELIVERY/`](../../P02-SUPPLIER-DELIVERY/).
  * Stock reorder parameters: Handed off from [`../P03-REPLENISHMENT/`](../../P03-REPLENISHMENT/).
- **Downstream Treasury Boundary:**  
  * Payment execution, cash disbursement, and bank reconciliation remain strictly outside P04 agent authority.
