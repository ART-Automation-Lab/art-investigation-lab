# Operational Workflow: Inventory Replenishment & Reorder Exceptions (P03-REPLENISHMENT)

> **Process ID:** `P03-REPLENISHMENT`  
> **Process Owner:** Bhushan  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)

---

## 1. As-Is Operational Workflow Topology

```text
[Continuous Inventory Consumption / Sales Orders]
                         │
                         ▼
   [WF-P03-001: Net Requirements & ROP Evaluation]
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      [Stock Above ROP]      [Reorder Triggered: Stock <= ROP]
             │                       │
      [No Action / Normal]           ▼
                       [WF-P03-002: Exception Filter & Constraint Check]
                       (MOQ, Order Pack Multiples, Vendor Lead Times)
                                     │
                         ┌───────────┴───────────┐
                         ▼                       ▼
                  [Standard Reorder]      [Exception Identified]
                         │                       │
                         │                       ▼
                         │           [WF-P03-003: Exception Triage & Planner Review]
                         │           (Lead-Time Surge, Allocation Cap, Demand Spike)
                         │                       │
                         ▼                       ▼
            [WF-P03-004: Purchase Requisition (PR) Generation]
                         │
                         ▼
            [WF-P03-005: Buyer Conversion to Purchase Order]
                         │
                         ▼
                 [PO Dispatched] ───► [P02-SUPPLIER-DELIVERY]
```

---

## 2. Detailed Step Specifications

### `WF-P03-001`: Net Requirement & Stock Position Calculation
- **Trigger:** Nightly MRP batch run or continuous event-driven replenishment monitor.
- **System / Operator:** ERP MRP Engine / Material Planner.
- **Formula:** Available Stock = On-Hand + Open POs (In-Transit) - Allocated Demand - Safety Stock.
- **Condition:** If Available Stock <= Reorder Point (ROP), generate order proposal.

### `WF-P03-002`: Exception Filtering & Supplier Constraints Check
- **Operator:** Inventory Analyst / System Validator.
- **Activities:** Validate replenishment quantity against supplier Minimum Order Quantities (MOQ), pallet/pack multiples, maximum warehouse storage limits, and shelf-life constraints.

### `WF-P03-003`: Exception Triage & Manual Planner Intervention
- **Operator:** Senior Inventory Planner.
- **Activities:** Review items flagged for:
  - Unexpected demand spikes (outliers vs. sustained growth).
  - Supplier lead-time variance reported by [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/).
  - Supplier allocation quotas (e.g., supplier rationing orders to 80% of normal).
- **Decision:** Manually adjust reorder quantity, split across dual vendors, or approve emergency spot purchase.

### `WF-P03-004`: Purchase Requisition (PR) Generation & Approval
- **System / Operator:** ERP Workflow / Department Budget Approver.
- **Activities:** Generate formal PR with required delivery date, account assignment, and delivery plant; route for budget sign-off.

### `WF-P03-005`: Conversion to PO & Handoff to Supplier Tracking
- **Operator:** Tactical Procurement Buyer.
- **Activities:** Convert approved PR to Purchase Order (PO); attach contract terms from [`../P01-RFP/`](../P01-RFP/); dispatch to vendor.
- **Handoff:** Transmit PO to [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/) for acknowledgment and delivery milestone tracking.

---

## 3. Cross-Process Boundaries & Dependencies

- **Upstream from P01 (RFP):** Consumes agreed supplier contracted lead times, pricing tiers, and minimum purchase commitments from [`../P01-RFP/`](../P01-RFP/).
- **Coupled with P02 (Supplier Delivery):** Delivery delays and partial shipments from [`../P02-SUPPLIER-DELIVERY/`](../P02-SUPPLIER-DELIVERY/) immediately distort available stock projections, triggering emergency reorder cycles.
- **Downstream to P04 (Invoice Exceptions):** Purchase order pricing tiers and unit quantities set the baseline for invoice 3-way matching in [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/).

---

## 4. References & Documentation

- Investigation Brief: [`investigation.md`](./investigation.md)
- Evidence Log: [`evidence.md`](./evidence.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
