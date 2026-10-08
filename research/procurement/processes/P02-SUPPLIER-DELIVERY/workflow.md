# Operational Workflow: Supplier Delivery Confirmation & Delay Escalation (P02-SUPPLIER-DELIVERY)

> **Process ID:** `P02-SUPPLIER-DELIVERY`  
> **Process Owner:** Vrushali  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)

---

## 1. As-Is Operational Workflow Topology

```text
[PO Issued to Supplier] (EDI / Email / Portal)
             │
             ▼
   [WF-P02-001: PO Transmission & Delivery Acknowledgment Clock]
             │
    ┌────────┴────────┐
    ▼                 ▼
[Acknowledged]    [Unacknowledged > 48h] ───► [WF-P02-002: Chaser Notification]
    │                                                   │
    ▼                                                   ▼
[WF-P02-003: EDD Verification & Feasibility Check] ◄────┘
    │
    ├────────────────────────┐
    ▼                        ▼
[On-Schedule]          [Delay Detected / Reschedule Request]
    │                        │
    │                        ▼
    │         [WF-P02-004: Impact Triage & Buffer Analysis]
    │                        │
    │            ┌───────────┴───────────┐
    │            ▼                       ▼
    │     [Buffer Absorbed]       [Stockout Risk / Critical Delay]
    │            │                       │
    │            │                       ▼
    │            │           [WF-P02-005: Tiered Escalation]
    │            │           (Expediting / Dual-Sourcing / Legal SLA Penalty)
    │            │                       │
    │            ▼                       ▼
    └────► [WF-P02-006: In-Transit ASN & Tracking Gate]
                 │
                 ▼
          [Dock Receiving] ───► Handoff to P03 (Inventory) & P04 (Invoice Match)
```

---

## 2. Detailed Step Specifications

### `WF-P02-001`: PO Transmission & Acknowledgment SLA
- **Trigger:** PO released and sent to vendor.
- **Operator:** Purchasing Specialist / Buyer.
- **Activities:** Dispatch PO via EDI 850 or automated PDF email; start the 48-hour acknowledgment countdown timer.

### `WF-P02-002`: Unacknowledged Order Follow-Up (Chasing)
- **Operator:** Procurement Expediter.
- **Activities:** Automated email reminder at T+48 hours; phone follow-up at T+72 hours; log vendor unresponsive state in ERP.

### `WF-P02-003`: Estimated Delivery Date (EDD) Verification
- **Operator:** Expediter / Supplier Portal Coordinator.
- **Activities:** Compare vendor-confirmed delivery date against PO required delivery date and contractual lead time. Flag date slippage or partial lot shipment.

### `WF-P02-004`: Production Impact Analysis & Buffer Calculation
- **Operator:** Material Planner / Expediter.
- **Activities:** Check current stock levels against promised EDD. If safety stock buffer is breached, calculate lead time to stockout.
- **Handoff:** Notify [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/) of confirmed date changes.

### `WF-P02-005`: Tiered Escalation & Alternative Sourcing
- **Operators:** Procurement Category Manager, Supply Chain Director.
- **Activities:** Level 1: Supplier account manager call; Level 2: Executive escalation and SLA penalty notice; Level 3: Authorize emergency premium freight or secondary supplier split.

### `WF-P02-006`: Advance Shipping Notice (ASN) & Dock Gate Handoff
- **Operator:** Inbound Logistics Coordinator.
- **Activities:** Receive EDI 856 ASN; track carrier bill of lading (BOL); verify shipment arrival at physical receiving dock.

---

## 3. Cross-Process Boundaries & Dependencies

- **Upstream from P01 (RFP):** Incorporates delivery lead times, carrier routing guides, and liquidated damage SLA terms negotiated in [`../P01-RFP/`](../P01-RFP/).
- **Downstream to P03 (Replenishment):** Feeds real-time delivery dates and partial-lot flags to [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/) to prevent stockouts.
- **Downstream to P04 (Invoice Exceptions):** Dock delivery confirmations and Goods Receipt Notes (GRN) supply the physical proof required for 3-way matching in [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/).

---

## 4. References & Documentation

- Investigation Brief: [`investigation.md`](./investigation.md)
- Evidence Log: [`evidence.md`](./evidence.md)
- ART Agent Validation: [`art-validation.md`](./art-validation.md)
