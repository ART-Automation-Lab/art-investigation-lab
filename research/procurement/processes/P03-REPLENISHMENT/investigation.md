# Investigation: Inventory Replenishment & Reorder Exceptions (P03-REPLENISHMENT)

> **Process ID:** `P03-REPLENISHMENT`  
> **Process Name:** Inventory Replenishment & Reorder Exceptions  
> **Process Owner:** Bhushan (Process Owner)  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)  
> **Master Prompt:** [`../../MASTER_PROMPT.md`](../../MASTER_PROMPT.md)  
> **Current Epistemic Level:** Baseline Initialized (`E0` hypotheses, unverified)

---

## 1. Process Scope & Operational Boundary

### In-Scope:
- Continuous monitoring of stock on-hand, open orders, and allocated demand across distribution centers and manufacturing plants.
- Evaluation of inventory against dynamic Reorder Points (ROP) and safety stock thresholds.
- Exception detection: demand surges, lead-time variance from suppliers, stockout risks, and minimum order quantity (MOQ) conflicts.
- Replenishment purchase requisition (PR) generation and supplier allocation optimization.
- Mitigation of the bullwhip effect through demand signal smoothing and historical seasonality review.

### Out-of-Scope (Handoffs):
- Master supplier contract negotiation and terms of trade (managed in [`../P01-RFP/`](../P01-RFP/)).
- Tracking PO shipment in-transit and carrier expediting (managed in [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/)).
- Supplier billing, 3-way matching, and payment release (managed in [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/)).

---

## 2. Core Investigation Questions

1. **MRP Exception Fatigue:** Why do inventory planners routinely experience "MRP alert fatigue" with thousands of daily system-generated reschedule/cancel messages, leading to ignored alerts?
2. **Dynamic Lead-Time Deficits:** How do standard enterprise inventory engines (SAP IBP, Oracle NetSuite, Blue Yonder) adapt when actual supplier delivery lead time diverges significantly from static system master data?
3. **Emergency Expediting Costs:** What is the annual organizational cost incurred by reactive stockout mitigation (spot buys, split orders, express freight) compared to proactive replenishment adjustments?
4. **Safety Stock Distortion:** How do planners handle contradictory demand signals during seasonal or market disruptions without artificially inflating safety stock?

---

## 3. Incumbent Software Landscape & Automation Deficits

| Software Category | Typical Vendors | Current Automation Capabilities | Critical Failure Points & Manual Deficits |
|---|---|---|---|
| **Advanced Planning & Scheduling (APS)** | SAP Integrated Business Planning (IBP), Blue Yonder, Kinaxis RapidResponse | Multi-echelon inventory optimization (MEIO), statistical demand forecasting, rough-cut capacity planning. | Highly complex mathematical models require pristine clean master data; planners frequently override recommendations via offline Excel sheets due to unmodeled real-world disruptions. |
| **Core ERP Material Requirements Planning (MRP)** | SAP S/4HANA (MRP Live), Oracle Cloud SCM | Batch replenishment proposals based on static Min-Max and fixed lead times. | Assumes deterministic lead times; cannot anticipate supplier delivery bottlenecks or dynamic logistics disruptions. |
| **Warehouse & Inventory Management** | Manhattan Associates, Körber, Blue Yonder WMS | Real-time bin tracking, cycle count verification, pick/pack automation. | Tracks physical inventory inside the four walls, but detached from supplier upstream production and transport delays. |

---

## 4. Operational Failure Modes & High-Consequence Risks

- **Critical Stockouts:** Running out of essential raw materials or high-velocity SKUs halts manufacturing lines or results in unfulfilled customer orders and contractual penalties.
- **Excess Working Capital & Scrap:** Panicked over-ordering in response to perceived shortages leads to warehouse congestion, cash flow drain, and inventory obsolescence/write-downs.
- **Supplier Allocation Lockout:** Delayed reorders during high-demand periods push the enterprise to the back of the supplier's allocation queue.

---

## 5. Investigation Next Steps & Artifact References

- Evidence Log: [`evidence.md`](./evidence.md)
- Operational Workflow Map: [`workflow.md`](./workflow.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
- Central Ambiguity Log: [`../../AMBIGUITIES.md`](../../AMBIGUITIES.md)
