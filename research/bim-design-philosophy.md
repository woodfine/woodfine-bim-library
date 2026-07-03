# BIM design philosophy

The Building Design System is built on a single architectural stance:
flat-file storage, open standards, offline-first operation — are not
stylistic choices. They are the precise set of constraints that turn
five common weaknesses in cloud-authoritative BIM platforms into
customer-visible differentiators.

Hyperscalers (Autodesk, Bentley, Trimble, and the broader IWMS
incumbents like Planon, IBM Tririga, Eptura Archibus) sell different-
looking products that share an identical architectural spine. Five
foundational assumptions underpin all of them, each one
simultaneously a revenue mechanism and a structural vulnerability:

1. The authoritative database lives in the vendor's multi-tenant cloud.
2. Access to the customer's own data requires a live subscription
   check.
3. Interoperability is achieved through lossy export/import, not
   native format.
4. AI must run in vendor tenancy on vendor-controlled data.
5. The economic unit is the seat, or the token, per month.

A sixth — version lock (Revit 2025 cannot open in 2024) — is
arguably the most effective lock-in mechanism ever shipped in AEC
software. The flat-file BIM substrate refuses each of these by
construction.

## What the substrate is

A directory of plain-text and standardised-binary files that an
ordinary text editor or SVG viewer can open without a proprietary
SDK, decades after the software vendor that produced it is gone.

| Format | ISO / publisher | Role |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Authoritative geometry + semantics |
| IDS 1.0 | buildingSMART (June 2024) | Validation contract |
| BCF 3.0 | buildingSMART | Per-topic collaboration history |
| COBie via ifccsv | NIST | Asset handover spreadsheet |
| Per-element YAML sidecars | local convention | Pset_* + sensor + work-order |
| Speckle-inspired object store | local convention | Hash-addressed Merkle DAG |
| glTF 2.0 | ISO/IEC 12113:2022 | Visualization cache (regenerable) |
| SVG | ISO/IEC 14496-22:2019 | 2D drawings (regenerable) |
| CityJSONSeq | OGC | Portfolio / urban context |

The building's authoritative state is the `.ifc` file plus the
sidecars. Visualisation derivatives are caches; they regenerate at
will from the authoritative source. Any specific BIM viewer or BIM
authoring tool is replaceable; the archive is permanent.

## What the substrate is NOT

- Not an authoring tool. The Workplace authoring application is
  layered on top of the substrate, not part of it.
- Not a SaaS platform. Every byte lives on the customer's hardware.
  No cloud dependency.
- Not vendor-prescriptive. Open standards and open toolchains
  throughout. The convergence layer (BIM + lease + ledger) and the
  City Code as Composable Geometry overlay are additive; the
  substrate itself is open.

## Five hyperscaler-incompatible capabilities

1. **Asset-anchored BIM** — the digital twin signed with the land
   title and travelling with the property deed. Multi-tenant SaaS
   cannot offer this without breaking the tenancy model.
2. **Offline-capable BIM for field use** — basements, rooftops,
   air-gapped defence facilities, healthcare campuses. Comparable
   cloud-authoritative platforms cannot work offline by construction.
3. **Vendor-obsolescence-survivable BIM** — buildings live 50+ years;
   proprietary CAD file formats last a fraction of that. The
   flat-file archive outlives the vendor by decades.
4. **IoT integration directly into the BIM archive** — per-element
   YAML sidecars ingest sensor readings via a local broker. No
   cloud intermediary; data never leaves the owner's premises.
5. **Convergence of BIM + lease register + financial ledger** — for
   a property owner, these are the same asset. Multi-tenant cloud
   cannot commingle them by construction.

## Government regulatory acceptance

The format stack — IFC-SPF + IDS 1.0 + BCF 3.0 + COBie — fulfills the
mandatory open-standard delivery requirements across US federal
(GSA, USACE, VA, NAVFAC), EU member states (Germany, Italy, Spain,
Denmark, Norway, Netherlands, Poland), the UK BIM Framework, Singapore
CORENET X (mandatory October 2026), Dubai (mandatory since January
2024), and emerging Latin-American mandates.

The offline-first, flat-file architecture is intended to natively
satisfy ITAR air-gapped requirements for defence projects, EU Data Act
data sovereignty for European projects, HIPAA technical safeguards for
healthcare facilities, and GDPR data residency for EU government
clients. Certification path under consideration: buildingSMART IFC
certification, buildingSMART openBIM software certification, and CMMC
Level 2 readiness documentation.

## References

- Autodesk Platform Services — https://aps.autodesk.com/
- Bentley iTwin.js — https://www.itwinjs.org/
- Trimble Connect — https://connect.trimble.com/
