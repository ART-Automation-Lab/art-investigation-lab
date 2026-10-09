# ERPNext Data Inventory: P04 Invoice Discrepancy Resolution

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Instance URL:** `https://bixbytessolutions.m.frappe.cloud`  
> **API Base:** `https://bixbytessolutions.m.frappe.cloud/api`  
> **Process Owner:** Ashwin (`ashwinash19`)  
> **Last Verification Date:** 2026-10-09  
> **Status:** Post-Cleanup Baseline Validated (0 Masters, 0 Transactions)

---

## 1. Organization & Legal Entities

| DocType | Document Name / ID | Key Field Values | Query Source | Status |
|---|---|---|---|---|
| **Company** | `Aiotrix` | Default Currency: `INR`<br>Country: India | `erpnext_find_docs_list` (`doctype: "Company"`) | **VERIFIED (LIVE)** |

*Notes:* Legal entity is exactly `"Aiotrix"`. Prior demo company name `"Aiotrix (Demo)"` was renamed or consolidated.

---

## 2. Master Data Inventory

| DocType | Target Field / Name | Record Count | Query Coverage | Status | Operational Impact |
|---|---|---|---|---|---|
| **Supplier** | `name`, `supplier_group`, `is_frozen` | **2+ verified** | Full query (`limit: 10`) via `erpnext_list_supplier` | **VERIFIED (LIVE)** | `P02 Test Supplier`, `P04-Test-Coastal Industrial Components` available. |
| **Item** | `item_code`, `uom`, `is_purchase_item` | **2+ verified** | Full query (`limit: 10`) via `erpnext_find_docs_list` | **VERIFIED (LIVE)** | `P02-TEST-ITEM-001` (Nos, ₹1.00), `P03-TEST-ITEM-001` available. |
| **Warehouse** | `warehouse_name`, `company` | **5 (historical)** | Desk list / historical discovery | **PARTIALLY VERIFIED** | Standard receiving warehouse active for Aiotrix. |
| **Item Group** | `item_group_name` | **6 (historical)** | Desk list / historical discovery | **PARTIALLY VERIFIED** | Standard groups available for item categorization. |

---

## 3. Transaction Records Inventory

| DocType | Key Query Fields | Observed Count | Tool Used | Status | Impact on P04 |
|---|---|---|---|---|---|
| **Purchase Order** | `PUR-ORD-2026-00011` | **1 verified** | `erpnext_get_purchase_order`, `get_po_details` | **VERIFIED (LIVE)** | Submitted (`docstatus = 1`), 1 Nos @ ₹1.00 (`To Receive and Bill`). |
| **Purchase Receipt** | `PR-26-00001` | **1 verified** | `erpnext_get_purchase_receipt`, `erpnext_get_docs_list` | **VERIFIED (LIVE)** | Submitted (`docstatus = 1`), 1 Nos @ ₹1.00 (`To Bill`). |
| **Purchase Invoice** | `PINV-26-00007` | **1 verified** | `erpnext_get_purchase_invoice` | **VERIFIED (LIVE)** | Submitted (`docstatus = 1`), linked to `P02 Test Supplier`. |
| **Payment Entry** | `name`, `party`, `paid_amount` | **N/A** | Tool not present in catalog | **OUT OF SCOPE** | Payment execution restricted to Treasury. |
| **Journal Entry** | `name`, `voucher_type` | **N/A** | Tool not present in catalog | **OUT OF SCOPE** | Financial posting restricted to Finance. |

---

## 4. Query Coverage & Response Schema Verification

```text
[Frappe Cloud API via erpnext_p04_readonly]
       │
       ├── /api/resource/Supplier?limit_page_length=10 ───────────► Returns ["P02 Test Supplier", "P04-Test-Coastal..."]
       │
       ├── /api/method/frappe.client.get_list?doctype=Item ───────► Returns ["P02-TEST-ITEM-001", "P03-TEST-ITEM-001"]
       │
       ├── /api/resource/Purchase Order/PUR-ORD-2026-00011 ───────► Returns full PO JSON (docstatus=1, Qty=1, ₹1.00)
       │
       ├── /api/resource/Purchase Receipt/PR-26-00001 ────────────► Returns full PR JSON (docstatus=1, Qty=1, ₹1.00)
       │
       └── /api/resource/Purchase Invoice/PINV-26-00007 ──────────► Returns full PI JSON (docstatus=1)
```

*Response Structure Consistency:*
- Standard REST resources return root key `data` (`{"data": [...]}`).
- Whitelisted method calls (`frappe.client.get_list`) return root key `message` (`{"message": [...]}`).
- Both structures cleanly differentiate empty datasets (`[]`) from HTTP 404 or authorization failures.
