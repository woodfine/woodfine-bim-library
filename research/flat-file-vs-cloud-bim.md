# Flat-file BIM vs cloud-authoritative BIM

A point-by-point comparison of architectural stances. The flat-file
side describes the Building Design System; the cloud-authoritative
side describes Autodesk Tandem / ACC, Bentley iTwin Experience,
Trimble Connect, Nemetschek dTwin, and the broader IWMS incumbent
class (Planon, IBM Tririga, Eptura Archibus, IBM Maximo, FM:Systems,
Bentley AssetWise, EcoDomus, ONUMA).

## Where the data lives

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Authoritative database location | Vendor's multi-tenant cloud (Azure / AWS / Google Cloud) | Customer's hardware; bytes never leave |
| Replication model | Vendor-controlled across vendor regions | Customer-controlled; backup is `cp -r` |
| Subscription dependency | Yes — non-Snapshot iModels enforce live check | No — files open in any IFC-aware tool |
| Subscription-lapse posture | Tandem: "you will need to enter into a new Token Flex Term…" — twin disappears | Owner holds the files; permanent and unconditional access |
| Asset-deed transfer | Requires reonboarding to the new owner's tenant | Files travel with the deed |

**Deployment topology.** This is not a hypothetical architecture
choice — Woodfine's internal design-response deck specifies each
Woodfine Building running on its own independent virtual machine
rather than a shared multi-tenant platform: "The Prototypes for each
of the Woodfine Buildings will be set up on their own Virtual
Machines... implement both a Building Database and Materials
Database on independent servers, lightweight Virtual Machines, for
each Woodfine Building... the individual Virtual Machines for each
building would also collect the data from the IoT Devices —
Sensors." The same document frames this as "an independent BIM
Server for each of the Woodfine Buildings." *(Source: internal
design-response deck, CONSTRUCTION_2025_10_31.)*

## Who can see the data

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Vendor visibility | Vendor sees model + collaboration graph in plaintext | Vendor sees nothing |
| Cross-tenant isolation | Contractual + technical (vendor-administered) | Architectural (separate machines) |
| Customer-corpus AI training | Vendor terms determine | Customer choice; on-device only by default |
| GDPR data residency | Contractual (BCRs + SCCs + regional centers) | Architectural — data never leaves jurisdiction |
| HIPAA (VA healthcare BIM) | Requires Business Associate Agreement | No BAA — local storage |
| ITAR / classified workflows | Cannot host CUI on standard cloud (requires IL4-IL6 isolation) | Native — data never leaves customer hardware |

## Operational continuity

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Internet dependency | Required | Optional — full functionality offline |
| Field use (basements, rooftops) | Read-only at best; usually broken | Native — no architectural change |
| Air-gapped facilities | Structurally impossible | Native |
| Construction-site network | Often unreliable; vendor productivity falls | No effect |
| Vendor outage | Customer is offline | Customer continues operating |
| Customer's vendor goes bankrupt | Twin evaporates as billing stops | Files remain readable for decades |

## Pricing models

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Economic unit | Seat, token, project | Outright purchase / subscription / EUPL-1.2 free |
| Marginal cost of additional users | Per seat, per month | Zero |
| Marginal cost of additional models | Per Forge token, per Tandem twin | Zero |
| Marginal cost of additional sensors | Often per-sensor charges | Zero — local MQTT broker |
| Renewal-rate exposure | Hyperscaler price-cap expiry triggers shock | None |
| TCO over 30-year asset life | Effectively unbounded | One-time + maintenance |

Woodfine's own stated rationale for this cost model: "With our own
Operating System we end up with a single integration cost per
building that we can amortize... avoids per-seat pricing or software
bloat. It's infrastructure — not overhead." *(Source: internal
design-response deck, CONSTRUCTION_2025_10_31.)*

## Format permanence

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| File format lifetime | Revit ~3 years (version lock) | IFC 2x3 + 4 + 4.3 (ISO 16739-1:2024) — 30+ years |
| Vendor-obsolescence | Twin evaporates | Files remain readable |
| Cross-version interop | Lossy export/import | Native — IFC is the schema |
| Buildable-tool diversity | Vendor SDK monoculture | Multiple parsers — IfcOpenShell, web-ifc, ifc_rs, xBIM, JSDAI, STEPcode |

## Convergence with non-BIM data

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Lease register integration | Separate IWMS subscription | Per-IfcSpace YAML sidecar |
| Financial ledger integration | Separate ERP integration (often broken) | Per-element sidecar links to project-bookkeeping vault |
| Sensor / IoT integration | Cloud intermediary (vendor-controlled) | Local MQTT broker → per-element sidecar |
| Work-order integration | Separate CMMS subscription | Per-element sidecar |
| Document integration | Separate document-management SaaS | Per-element sidecar references the document vault |

The fifth hyperscaler-incompatible capability — convergence in one
portable archive — is the strategically novel one. For a property
owner, BIM + lease register + financial ledger are the same asset.
Multi-tenant cloud cannot commingle them; commercial confidentiality,
data residency, financial-audit trails, and multi-tenant isolation
all prevent it. The flat-file substrate makes them one thing by
construction.

## What flat-file BIM does NOT do well (yet)

Honest accounting:

- **Real-time multi-user editing** — git-style merging works for
  authoring workflows but is slower than real-time collaborative
  editing for design-charette-style workshops. Cloud SaaS is genuinely
  better for synchronous design sessions; PointSav's offline-first
  posture is the trade-off accepted.
- **Massive city-scale federation** — the flat-file substrate scales
  to a portfolio of buildings; full city-scale digital twins (1M+
  buildings) need a different streaming architecture.
- **Generative AI BIM authoring** — Project Bernini-class generative
  3D foundation models are vendor-closed today. The substrate is
  AI-ready (Doorman dispatches AS-2 grammar substrate; service-slm
  routes generative requests through the audit ledger) but PointSav
  does not ship a generative BIM authoring tool at v0.0.1. v0.0.2+.

## References

- Autodesk Platform Services token pricing — https://aps.autodesk.com/
- Bentley iTwin.js — https://www.itwinjs.org/
- Trimble Connect — https://connect.trimble.com/
- Planon EasyFlow (Feb 2026 mid-market launch) — https://planonsoftware.com/
