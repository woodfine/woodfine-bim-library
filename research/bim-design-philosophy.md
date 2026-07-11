# BIM design philosophy

The Building Design System is built on a single architectural stance:
flat-file storage, open standards, offline-first operation — are not
stylistic choices. They are the precise set of constraints that turn
five common weaknesses in cloud-authoritative BIM platforms into
customer-visible differentiators.

Commercial cloud-authoritative BIM platforms and the broader IWMS
incumbent category sell different-looking products that share an
identical architectural spine. Five foundational assumptions
underpin all of them, each one simultaneously a revenue mechanism
and a structural vulnerability:

1. The authoritative database lives in the vendor's multi-tenant cloud.
2. Access to the customer's own data requires a live subscription
   check.
3. Interoperability is achieved through lossy export/import, not
   native format.
4. AI must run in vendor tenancy on vendor-controlled data.
5. The economic unit is the seat, or the token, per month.

A sixth — version lock, where a file saved in one software release
cannot open in an earlier release of the same product — is arguably
the most effective lock-in mechanism in wide use in AEC software.
The flat-file BIM substrate refuses each of these by construction.

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
| SVG 2 | W3C Recommendation | 2D drawings (regenerable) |
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

## Why build, not buy

The case against licensing a hyperscaler's platform instead of
building the flat-file substrate was made internally, by Woodfine,
before this document existed:

On vendor heterogeneity: "Most buildings are filled with equipment
from multiple vendors, all speaking different languages, and running
separate firmware. Some devices can't be updated. Others can, but
only through vendor calls and consulting agreements. It's not
efficient. It's not accountable."

On the cost model: "With our own Operating System we end up with a
single integration cost per building that we can amortize... Ongoing
support fits into Operating Costs and avoids per-seat pricing or
software bloat. It's infrastructure — not overhead."

On control: "If we do not develop the software ourselves, we will
never really have control over it" — and, on the counterfactual of
building on someone else's platform: "One downside of using Microsoft
Windows as the base of our Operating Systems is that we would no
longer be in control of the technology underpinning the delivery of
our Digital Twin."

The intent for the BIM layer specifically was stated the same way:
"The Control Architect will be responsible for ensuring all data is
compatible, working towards an open-sourced Building Information
Modelling (BIM) run time, which should allow for compatibility with
any software the Collaborators require." Woodfine's original framing
called for "an independent BIM Server for each of the Woodfine
Buildings... Hopefully, we will be able to use an Open BIM, allowing
for full access amongst all the Collaborators, regardless of their
particular software selections" — targeting buildingSMART's ISO
19650 certification. The flat-file substrate is the realization of
that stated intent, not a retrofit narrative built after the fact.

*Source: internal design-response deck, CONSTRUCTION_2025_10_31.*

## Five hyperscaler-incompatible capabilities

1. **Asset-anchored BIM** — the digital twin signed with the land
   title and travelling with the property deed. Multi-tenant SaaS
   cannot offer this without breaking the tenancy model.
2. **Offline-capable BIM for field use** — basements, rooftops,
   air-gapped defence facilities, healthcare campuses. Comparable
   cloud-authoritative platforms cannot work offline by construction.
3. **Vendor-obsolescence-survivable BIM** — buildings live 50+ years
   (Woodfine's internal design-response deck targets 100+ years for
   its own buildings specifically); proprietary CAD file formats
   last a fraction of that. The flat-file archive outlives the
   vendor by decades.
4. **IoT integration directly into the BIM archive** — per-element
   YAML sidecars ingest sensor readings via a local broker. No
   cloud intermediary; data never leaves the owner's premises.
5. **Convergence of BIM + lease register + financial ledger** — for
   a property owner, these are the same asset. Multi-tenant cloud
   cannot commingle them by construction.

## Government regulatory acceptance

The format stack — IFC-SPF + IDS 1.0 + BCF 3.0 + COBie — satisfies
open-standard delivery requirements already in force across US
federal procurement (GSA, USACE, VA, NAVFAC), the UK's Information
Management Mandate (ISO 19650, mandatory for publicly funded
projects), Singapore's CORENET X framework (mandatory for all new
building projects from October 2026), and Dubai's BIM mandate
(mandatory since January 2024). Adoption across the European Union
is uneven by member state and growing — Denmark has required BIM on
public procurement since 2007 and Spain since 2018, while several
other member states are still phasing in national programmes.

The offline-first, flat-file architecture is intended to natively
satisfy ITAR air-gapped requirements for defence projects, EU Data Act
data sovereignty for European projects, HIPAA technical safeguards for
healthcare facilities, and GDPR data residency for EU government
clients. Certification path under consideration: buildingSMART IFC
certification, buildingSMART openBIM software certification, and CMMC
Level 2 readiness documentation.

## References

- IFC 4.3 — Industry Foundation Classes (ISO 16739-1:2024), buildingSMART International
- Information Delivery Specification (IDS) 1.0, buildingSMART International
- BIM Collaboration Format (BCF) 3.0, buildingSMART International
- COBie v3 — Construction Operations Building Information Exchange, National Institute of Building Sciences
