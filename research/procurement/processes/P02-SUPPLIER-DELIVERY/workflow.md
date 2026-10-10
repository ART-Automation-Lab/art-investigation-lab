# Operational Workflow: Supplier Delivery Confirmation & Delay Escalation (P02-SUPPLIER-DELIVERY)

> **Process ID:** `P02-SUPPLIER-DELIVERY`  
> **Process Owner:** Vrushali  
> **Governing Standard:** [`../../RESEARCH_STANDARD.md`](../../RESEARCH_STANDARD.md)
> **Last Updated:** 2026-10-09 (Phase 1 Review Corrections)

---

## 1. As-Is Operational Workflow Topology

```text
[PO Issued to Supplier] (EDI 850 / Email / Portal)
             │
             ▼
   [WF-P02-001: PO Transmission & Delivery Acknowledgment Clock]
             │
    ┌────────┴────────┐
    ▼                 ▼
[Acknowledged]    [Unacknowledged > 48h] ───► [WF-P02-002: Staged Chaser Drafting]
    │                                                   │
    ▼                                                   ▼
[WF-P02-003: Delivery Date & Quantity Reconciliation Gate] ◄┘
    │
    ├────────────────────────┬────────────────────────┐
    ▼                        ▼                        ▼
[On-Schedule Full]     [Partial Split / Backorder]  [Delay Detected / Reschedule Request]
    │                        │                        │
    │                        │                        ▼
    │                        │         [WF-P02-004: Buffer & Production Impact Triage]
    │                        │                        │
    │                        │            ┌───────────┴───────────┐
    │                        │            ▼                       ▼
    │                        │     [Buffer Absorbed]       [Stockout Risk / Critical Breach]
    │                        │            │                       │
    │                        │            │                       ▼
    │                        │            │           [WF-P02-005: Tiered Escalation]
    │                        │            │           (Expediting / Dual-Sourcing / SLA Notice)
    │                        │            │                       │
    │                        ▼            ▼                       ▼
    └────────────────► [WF-P02-006: In-Transit ASN & Dock Gate Handoff]
                                 │
                                 ▼
                          [Dock Receiving] ───► Handoff to P03 (Inventory) & P04 (Invoice Match)
```

---

## 2. Detailed Step Specifications

### `WF-P02-001`: PO Transmission & Acknowledgment SLA Clock
- **Trigger:** Approved Purchase Order dispatched to supplier via EDI 850, ERP email connector, or vendor portal.
- **Operator:** Purchasing Specialist / Automated ERP Dispatcher.
- **Inputs:** Released Purchase Order document, Vendor Email/EDI Endpoint, Requested Delivery Date (`RDD`), Incoterms.
- **Activities:** Dispatch PO payload; start the 48-hour acknowledgment countdown timer (`SLA-ACK-48H`).
- **Outputs:** Timestamped dispatch record; active monitoring queue entry.
- **Evidence Reference:** ANSI ASC X12 850/855 standards ([`evidence.md#evd-p02-002`](./evidence.md)).

### `WF-P02-002`: Unacknowledged Order Follow-Up (Staged Chaser Drafting)
- **Trigger:** Timer expires at T+48 hours with zero incoming acknowledgment record.
- **Operator:** Procurement Expediter / Automated Chaser Agent.
- **Inputs:** Open PO record, vendor contact profile, days elapsed.
- **Activities:** Generate a staged draft inquiry for supplier sales contact (`auto_send: false`). At T+72 hours without response, assign expediter task card for phone outreach.
- **Outputs:** Staged draft chaser record; expediting priority queue update. Zero autonomous outbound emails are dispatched.
- **Evidence Reference:** Expediting operational burden ([`evidence.md#evd-p02-004`](./evidence.md)).

### `WF-P02-003`: Delivery Date & Quantity Reconciliation Gate
- **Trigger:** Vendor response received (EDI 855 message, unstructured email body, or PDF confirmation).
- **Operator:** Expediter / Supplier Response Parser Agent.
- **Inputs:** Supplier confirmation payload, ERP PO baseline schedule line.
- **Activities:**
  1. Extract Promised Delivery Date (`PDD`), promised line quantities, and status code.
  2. Reconcile against baseline PO:
     - Scenario A: Full acceptance on-schedule (`IA` status) $\rightarrow$ Stage schedule line update for ingestion buffer (`STAGE_SCHEDULE_LINE_UPDATE`).
     - Scenario B: Partial shipment committed (`BP` status) $\rightarrow$ Calculate backorder quantity, stage split schedule lines (`EKET`), route to `WF-P02-004` and human review.
     - Scenario C: Date slippage (`PDD > RDD`) $\rightarrow$ Calculate variance in business days, stage revised date, route to `WF-P02-004` and human review.
     - Scenario D: Ambiguous or conflicting response $\rightarrow$ Halt automated processing; stage draft clarification; route to Human Review Gate.
     - Scenario E: Contractual alteration (price increase, part substitution) $\rightarrow$ Halt workflow; enforce strict prohibition against price/SKU modification; route to commercial buyer.
- **Outputs:** Normalized structured confirmation payload; discrepancy classification.
- **Safety Invariant:** Zero direct unverified ERP writes. All actions are staged.
- **Evidence Reference:** ANSI ASC X12 855 ACK Codes ([`evidence.md#evd-p02-002`](./evidence.md)), SAP Confirmation Control Keys ([`evidence.md#evd-p02-003`](./evidence.md)).

### `WF-P02-004`: Buffer & Production Impact Triage
- **Trigger:** Confirmed delay or split delivery received from `WF-P02-003`.
- **Operator:** Material Planner / Inventory Replenishment Specialist.
- **Inputs:** Revised delivery date, material part number, current on-hand inventory, daily consumption rate / safety stock threshold.
- **Activities:** Compute projected inventory level on original `RDD` vs. new `PDD`. Determine whether safety stock buffer absorbs the delay or whether stockout occurs.
- **Outputs:** Impact classification (`BUFFER_ABSORBED` vs. `STOCKOUT_RISK`); handoff trigger to [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/).

### `WF-P02-005`: Tiered Escalation & Alternative Sourcing
- **Trigger:** `STOCKOUT_RISK` or unmitigated delay exceeding operational tolerance.
- **Operators:** Procurement Category Manager, Supply Chain Director.
- **Activities:**
  - **Tier 1:** Supplier account manager negotiation for production prioritization.
  - **Tier 2:** Supplier-funded expedited air freight authorization to recover transit days.
  - **Tier 3:** Emergency purchase split from secondary qualified vendor (handoff to P03).
  - **Tier 4:** Issuance of formal SLA liquidated damages penalty or breach notice based on contract terms negotiated in P01.
- **Outputs:** Escalation log; authorized recovery action plan; ERP revision record.
- **Evidence Reference:** Incoterms risk allocation ([`evidence.md#evd-p02-005`](./evidence.md)).

### `WF-P02-006`: Advance Shipping Notice (ASN) & Dock Gate Handoff
- **Trigger:** Goods dispatched from vendor facility.
- **Operator:** Inbound Logistics Coordinator.
- **Inputs:** EDI 856 ASN, carrier Bill of Lading (BOL), GPS/container tracking milestone data.
- **Activities:** Match ASN to PO schedule line; monitor carrier milestones; notify warehouse receiving team.
- **Outputs:** Verified inbound delivery document (`LA` confirmation in ERP); handoff to physical dock receiving.
- **Handoff:** Downstream handoff to [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/) for stock availability and [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/) for 3-way matching goods receipt note (GRN).

---

## 3. Cross-Process Boundaries & Dependencies

- **Upstream from P01 (RFP):** Ingests negotiated supplier lead times, carrier routing compliance rules, and liquidated damage SLA terms negotiated in [`../P01-RFP/`](../P01-RFP/).
- **Downstream to P03 (Replenishment):** Transmits confirmed delivery dates, split lots, and lead-time delays to [`../P03-REPLENISHMENT/`](../P03-REPLENISHMENT/) to trigger safety stock recalculations or emergency reorders.
- **Downstream to P04 (Invoice Exceptions):** Transmits confirmed delivery milestones and dock goods receipts to [`../P04-INVOICE-EXCEPTIONS/`](../P04-INVOICE-EXCEPTIONS/) to provide clean receiving lines for 3-way invoice matching.

---

## 4. References & Documentation

- Investigation Brief: [`investigation.md`](./investigation.md)
- Evidence Log: [`evidence.md`](./evidence.md)
- Benchmark Specification: [`benchmark-DELIVERY-001.md`](./benchmark-DELIVERY-001.md)
- ART Agent Validation Protocol: [`art-validation.md`](./art-validation.md)
