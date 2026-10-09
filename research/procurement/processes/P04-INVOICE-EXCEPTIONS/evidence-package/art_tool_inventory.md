# ART Tool & Provider Inventory: `erpnext_art`

> **Process ID:** `P04-INVOICE-EXCEPTIONS`  
> **Provider ID:** `erpnext_art`  
> **Connection Label:** `erpnext-newapi`  
> **Export Source:** `C:\Users\ashwi\Downloads\art-tool-provider-erpnext_art.json`  
> **Process Owner:** Ashwin (`ashwinash19`)  
> **Creation Date:** 2026-10-09  
> **Catalog Scope:** 38 total tools evaluated; audited against P04 procurement exception matching.

---

## 1. Provider Configuration

- **Provider Name:** `erpnext_art`
- **Label:** `ERPNext`
- **Base URL:** `https://bixbytessolutions.m.frappe.cloud/api`
- **Authentication Scheme:** Frappe Token Scheme (`token <api_key>:<api_secret>`)
- **Default Headers:** `{"Accept": "application/json"}`
- **Ownership Scope:** Tenant
- **Supported Platforms:** `['agent', 'orchestrator']`

---

## 2. P04 Core Tool Classification Matrix

| Tool ID | Method | Endpoint Pattern | Classification | Safety & P04 Suitability |
|---|---|---|---|---|
| `erpnext_get_purchase_order` | `GET` | `/resource/Purchase%20Order/{params.purchase_order_name}` | Read-Only | **SAFE & REQUIRED** — Retrieves line rates, ordered qty, received qty. |
| `erpnext_list_purchase_order` | `GET` | `/resource/Purchase%20Order?limit_page_length={params.limit}` | Read-Only | **SAFE & REQUIRED** — Discovers PO numbers. |
| `erpnext_get_purchase_receipt` | `GET` | `/resource/Purchase%20Receipt/{params.purchase_receipt_name}` | Read-Only | **SAFE & REQUIRED** — Retrieves receiving quantities and warehouse. |
| `erpnext_list_purchase_receipt` | `GET` | `/resource/Purchase%20Receipt?limit_page_length={params.limit}` | Read-Only | **SAFE & REQUIRED** — Discovers PR numbers. |
| `erpnext_get_purchase_invoice` | `GET` | `/resource/Purchase%20Invoice/{params.invoice_name}` | Read-Only | **SAFE & REQUIRED** — Retrieves billed rates, taxes, grand totals. |
| `erpnext_list_purchase_invoice` | `GET` | `/resource/Purchase%20Invoice?limit_page_length={params.limit}` | Read-Only | **SAFE & REQUIRED** — Discovers PI numbers. |
| `erpnext_get_supplier` | `GET` | `/resource/Supplier/{params.supplier_name}` | Read-Only | **SAFE & REQUIRED** — Retrieves supplier hold status and rules. |
| `erpnext_list_supplier` | `GET` | `/resource/Supplier?limit_page_length={params.limit}` | Read-Only | **SAFE & REQUIRED** — Lists suppliers for master discovery. |
| `erpnext_find_docs_list` | `GET` | `/method/frappe.client.get_list?doctype={params.doctype}&limit_page_length={params.limit}` | Read-Only | **SAFE & REQUIRED** — Discovers master documents (`Company`, `Item`). |
| `erpnext_get_docs_list` | `GET` | `/resource/{params.doctype}/{params.name}` | Read-Only | **SAFE & OPTIONAL** — Generic record retriever. |
| `erpnext_create_docs_list` | `POST` | `/resource/{params.doctype}` | Generic Write | **BLOCKED (DEFECTIVE)** — Body mapping defect `DEF-P04-001`. |
| `erpnext_update_docs_list` | `PUT` | `/resource/{params.doctype}/{params.name}` | Generic Write | **PROHIBITED** — Unrestricted mutation; violates SoD. |
| `create_purchase_order` | `POST` | `/resource/Purchase Order` | Specific Write | **RESTRICTED** — Single line PO creator; lacks company parameter. |
| `create_purchase_receipt` | `POST` | `/resource/Purchase Receipt` | Specific Write | **BLOCKED (DEFECTIVE)** — Hardcoded supplier defect `DEF-P04-002`. |
| `submit_purchase_receipt` | `PUT` | `/resource/Purchase Receipt/{params.pr_number}` | Consequential | **PROHIBITED FOR AGENT** — Autonomous document submission. |
| `expedite_purchase_order` | `PUT` | `/resource/Purchase Order/{params.po_number}` | Consequential | **PROHIBITED FOR AGENT** — Unrelated to invoice exception. |

---

## 3. Deep-Dive Defect Analysis

### Defect `DEF-P04-001`: Request Body Wrapping in `erpnext_create_docs_list`
* **Target Endpoint:** `POST {base.api}/resource/{params.doctype}`
* **Declared Parameter:** `data` (string: *"JSON object containing the document fields to create"*)
* **Actual Step Definition:**
  ```json
  "body": {
    "kind": "json",
    "value": {
      "description": "{params.data}"
    }
  }
  ```
* **Output Schema Keys:** `['assigned_by_full_name', 'creation', 'date', 'description', 'docstatus', 'doctype', 'idx', 'modified', 'modified_by', 'name']`
* **Defect Impact:**  
  1. The template nests the incoming JSON data inside a single field named `description`.
  2. For Frappe DocTypes requiring root-level dictionary fields (e.g. `Purchase Order` requiring `supplier`, `items`, `schedule_date`), Frappe rejects the request with `frappe.exceptions.MandatoryError`.
  3. The output schema is literally cloned from ERPNext's `ToDo` DocType.

### Defect `DEF-P04-002`: Hardcoded Supplier in `create_purchase_receipt`
* **Target Endpoint:** `POST {base.api}/resource/Purchase Receipt`
* **Actual Step Definition:**
  ```json
  "body": {
    "kind": "json",
    "value": {
      "items": [
        {
          "item_code": "{params.item_code}",
          "purchase_order": "{params.po_number}",
          "qty": "{params.qty}",
          "warehouse": "{params.warehouse}"
        }
      ],
      "posting_date": "{params.schedule_date}",
      "supplier": "MediSupply Healthcare Pvt Ltd"
    }
  }
  ```
* **Defect Impact:**  
  1. The tool ignores the supplier associated with `params.po_number`.
  2. Always submits `"MediSupply Healthcare Pvt Ltd"`, causing validation failure (`Supplier does not match Purchase Order`) for any test scenario using another supplier.

---

## 4. Agent Safety & Tool Exclusions

To enforce audit compliance, the P04 Autonomous Agent configuration must obey these tool assignments:

* **Assigned to Agent:** Read-only retrieval tools (`erpnext_get_*`, `erpnext_list_*`, `erpnext_find_docs_list`).
* **Excluded from Agent:**
  * All `POST` tools (`erpnext_create_docs_list`, `create_purchase_order`, `create_purchase_receipt`).
  * All `PUT` / `DELETE` tools (`erpnext_update_docs_list`, `submit_purchase_receipt`, `expedite_purchase_order`).
  * Any payment or disbursement API.
