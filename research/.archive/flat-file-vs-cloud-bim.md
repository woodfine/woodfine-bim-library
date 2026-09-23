# Flat-file BIM vs cloud-authoritative BIM

A point-by-point comparison of architectural stances. The flat-file
side describes the Woodfine BIM Library; the cloud-authoritative side
describes the multi-tenant cloud digital-twin platforms and
Integrated Workplace Management System (IWMS) products in wide
commercial use — a category, not any single product.

## Where the data lives

| Dimension | Cloud-authoritative BIM | Flat-file BIM |
|---|---|---|
| Authoritative database location | Vendor's multi-tenant cloud (Azure / AWS / Google Cloud) | Customer's hardware; bytes never leave |
| Replication model | Vendor-controlled across vendor regions | Customer-controlled; backup is `cp -r` |
| Subscription dependency | Yes — non-Snapshot iModels enforce live check | No — files open in any IFC-aware tool |
| Subscription-lapse posture | Published terms for one commercial digital-twin platform state that a lapsed license requires entering a new paid term before the twin is accessible again | Owner holds the files; permanent and unconditional access |
| Asset-deed transfer | Requires reonboarding to the new owner's tenant | Files travel with the deed |

**Deployment topology.** This is not a hypothetical architecture choice. Each of our buildings runs on its
own independent virtual machine rather than a shared multi-tenant platform — a Building Database and a
Materials Database on independent, lightweight servers per building, with each building's virtual machine
also collecting IoT sensor data directly. We treat this as an independent BIM Server for each of our
buildings. *(Internal design documentation, October 2025.)*

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
| Marginal cost of additional models | Per proprietary cloud token or twin instance | Zero |
| Marginal cost of additional sensors | Often per-sensor charges | Zero — local MQTT broker |
| Renewal-rate exposure | Hyperscaler price-cap expiry triggers shock | None |
| TCO over 30-year asset life | Effectively unbounded | One-time + maintenance |

Our rationale for this cost model: building our own operating system gives us a single integration cost
per building that we can amortize, avoiding per-seat pricing or software bloat. It's infrastructure, not
overhead. *(Internal design documentation, October 2025.)*

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
| Financial ledger integration | Separate ERP integration (often broken) | Per-element sidecar links directly to the property's financial ledger |
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

## Where flat-file BIM has limits

- **Real-time multi-user editing.** Git-style merging suits
  asynchronous authoring workflows but is slower than real-time
  collaborative editing for design-charette-style workshops. Cloud
  SaaS platforms are genuinely better suited to synchronous design
  sessions; the flat-file substrate accepts this trade-off in
  exchange for its offline-first posture.
- **Massive city-scale federation.** The flat-file substrate scales
  to a portfolio of buildings; full city-scale digital twins
  (1M+ buildings) need a different streaming architecture.
- **Generative AI BIM authoring.** Generative 3D foundation models
  capable of authoring BIM directly are vendor-closed today across
  the industry. The substrate is structured to accept generative
  output once such tooling matures, but does not ship a generative
  BIM authoring capability in the current release.

## References

- IFC 4.3 — Industry Foundation Classes (ISO 16739-1:2024), buildingSMART International
- IfcOpenShell — https://ifcopenshell.org
- EUPL v1.2 — European Union Public Licence
