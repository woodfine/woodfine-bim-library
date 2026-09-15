---
schema: journal-v2
slug: flat-file-bim-substrate
title: "Why We Store Building Data in Files We Own, Not a Vendor's Cloud"
subtitle: "An open-standard alternative to subscription-gated building information platforms"
site: bim.woodfinegroup.com
imprint: WCP-2026-05
thesis: "Commercial building-information platforms bundle five design choices — hosted data, subscription-gated access, lossy import/export, vendor-run analysis, and per-seat pricing — into one coupled architecture; an alternative built entirely on open, published standards and stored as plain files the owner holds outright delivers real capabilities that arrangement cannot provide by construction, at one honest cost: weaker real-time collaborative editing."
abstract: |
  When a building owner picks a building-information-modeling platform, they are picking an
  architecture, not just a feature set. The commercial products in wide use today share a
  consistent pattern: the authoritative record of the building lives in the vendor's own
  cloud, access requires an active subscription, moving data to another tool loses
  information in the process, and the pricing is per seat or per project, charged on an
  ongoing basis. None of these choices are unreasonable for a vendor funding software
  development — but together they mean a building owner's decades-long access to their own
  asset data ultimately depends on a vendor relationship staying intact. We describe an
  alternative built entirely on open, publicly published data standards, where the building's
  authoritative record is a directory of plain files the owner holds outright, and any
  authoring or viewing tool is a replaceable client of that record rather than its custodian.
  We identify five real capabilities this approach provides that the subscription-gated
  cloud approach cannot provide by construction — the record travels with a property sale
  the same way a deed does, it remains fully usable with no internet connection at all, it
  outlives any single software vendor's business lifespan, it accepts sensor data directly
  with no cloud intermediary, and it lets a single file structure hold the building data, the
  lease records, and the financial records together rather than as three separately licensed
  systems. We are equally direct about the one place this approach is weaker: real-time,
  many-person simultaneous editing, which a centrally-hosted platform handles better today.
  The argument is grounded in a real, currently operating deployment, not a hypothetical.
state: draft
version: "1.0.0"
published:
updated: "2026-09-15"
doi:
license: CC-BY-4.0
cites:
  - ifc-4-3
  - ids-1-0
  - bsdd-v1
  - iso-19650
  - iso-16739-2018
  - cobiev3
  - buildingsmart-bcf3
  - w3c-svg-2
  - khronos-gltf-2-iso-12113
  - eupl-1-2
  - gsa-bim-guide
  - va-bim-standard-manual
  - uk-bim-framework
  - corenet-x-2021
  - ifcopenshell-2025
  - ifc-fragment-spec
  - germany-bim-stufenplan
  - spain-bim-plan-2023
  - denmark-bim-ict-regulations
  - netherlands-rvb-bim-norm
  - poland-bim-status-2026
draws_from:
  - bim-design-philosophy
  - flat-file-vs-cloud-bim
  - os-workplace
contributors:
  - name: Peter M. Woodfine
    roles: [Founding Contributor]
  - name: Jennifer M. Woodfine
    roles: [Founding Contributor]
  - name: Mathew Woodfine
    roles: [Founding Contributor]
keywords:
  - flat-file BIM
  - open BIM standards
  - data ownership
  - offline-first architecture
  - asset lifecycle
  - vendor independence
---

## 1. The question

A building owner selecting a building-information-modeling platform is selecting an
architecture, not a feature list. The commercial products in production use today —
spanning dedicated digital-twin tools, cloud-native collaboration environments, and the
broader facility-management software category — converge on a consistent design: the
authoritative model lives in the vendor's own cloud infrastructure; using it requires an
active subscription at the time of use; moving data to a different tool goes through an
export/import step that loses information relative to the platform's own internal format;
and the ongoing cost is per seat, per token, or per project, billed continuously. None of
this is a defect in any individual vendor's product — each choice is a reasonable way to
fund software development and guarantee service levels. But a building has an operating
life measured in decades, often exceeding the working lifespan of the company that built the
software managing its data, and the five choices above compound over exactly that timescale.

This paper asks a narrower, testable question: are there capabilities a building owner
actually needs that an open-standard, owner-held alternative can provide and a
subscription-gated cloud platform cannot provide — not merely does not currently offer by
choice, but cannot provide as a structural consequence of where the data lives and who
controls access to it?

## 2. What we found

**Five owner-facing capabilities are structurally unavailable to a subscription-gated cloud
platform, not merely unoffered by current products.** A digital record that can be signed
over with a property deed requires the record to be something the owner unconditionally
possesses, not an entitlement tied to an active account — a cloud platform cannot offer this
without abandoning its own multi-tenant business model. Full read-and-write functionality
with no internet connection at all — needed in basements, remote sites, and
network-restricted facilities — requires the authoritative copy to already be local; a cloud
platform's authoritative copy is, by definition, not local. Surviving the eventual closure or
acquisition of the software vendor requires the file format itself to have a multi-decade
continuity guarantee independent of any one company — the open standard this architecture is
built on has already spanned more than two decades of managed revisions. Accepting sensor
data directly into the building's own record, with no cloud intermediary in the path,
requires the record to already be inside the same network boundary as the sensor. And
holding building data, lease records, and financial records together in one addressable
structure — rather than three separately licensed systems requiring point-to-point
integration — requires removing a multi-tenant boundary a shared-infrastructure vendor
cannot remove without breaking commercial confidentiality between its own customers.

**Each of the five properties in the commercial architecture is simultaneously a funding
mechanism and a limit on the owner's own control — the same feature does both jobs at
once.** This is the paper's central architectural observation: the coupling is not
accidental. A vendor-run subscription check funds the vendor's operations and also gates the
owner's own access; a lossy export format simplifies the vendor's product boundary and also
locks data inside it; vendor-side data processing enables vendor-offered analysis features
and also means the vendor sees everything.

**We found one place, stated directly, where the trade runs the other way.** Real-time,
many-person simultaneous editing — the kind used in fast-paced design workshops with several
people editing the same element at once — is measurably better served by a centrally
arbitrated, always-connected platform than by the version-control-style merging our
file-based approach uses. We accept this cost as the price of prioritizing offline-first
operation, and report it as a genuine weakness rather than minimizing it.

**Government building-code and procurement frameworks across several jurisdictions already
require conformance to the same open standards this architecture is built on, not to any
specific commercial platform.** Public building requirements in the United States, the
United Kingdom, Singapore, and Dubai each specify open, standards-based deliverables — none
names a commercial product. Adoption within the European Union varies meaningfully by
country and is stated here at real, individually verified status rather than as a uniform
claim: several countries mandate it for public work today, several have only partial or
planned mandates, and at least one has no national mandate at all.

## 3. How we built it

The architecture rests on a directory of plain-text and standardized-binary files, openable
by any ordinary text editor or standards-compliant viewer with no proprietary software
required, and legible decades after the specific application that produced any one file is
no longer maintained. The authoritative geometry and building data lives in the IFC open
standard (ISO 16739-1), accompanied by a published validation contract (IDS) that machine-
checks what a compliant model must contain, an open collaboration-issue format (BCF) for
tracking coordination items, and a standard asset-handover spreadsheet format for facility
management. Individual elements carry stable, tool-neutral identity codes from a shared
international dictionary, so an element's identity does not depend on which authoring tool
created it. Two visualization formats — one for 3D rendering, one for 2D drawing derivatives
— are regenerated deterministically from the authoritative source and carry no information
the source file does not already contain; they are caches, not additional sources of truth.

Any specific authoring or viewing application is, by this architecture, a replaceable client
of the underlying files — never their custodian. The building's authoritative state has no
dependency on any single application remaining in production. Extending the base
building-data files, we attach per-element sidecar records for property sets, sensor
readings, and work orders, and use a hash-addressed, content-verified object store — the
same structural idea behind modern version-control systems — for a complete, tamper-evident
history of every change, replicated by the owner across whatever infrastructure the owner
chooses, with a directory copy constituting a complete backup.

The comparative claims in §2 and the case for building rather than licensing this substrate
are grounded in a single, real, currently-operating multi-building deployment — a case study,
not a controlled experiment across multiple owners, and we say so plainly in §5. The
motivating rationale for building this substrate — vendor equipment heterogeneity across a
real building portfolio, the cost of recurring per-seat licensing at portfolio scale, and a
direct judgment that control over infrastructure this central to a decades-long asset
requires actually owning the software, not licensing it — predates this paper and was
recorded internally before the substrate existed, not written afterward to justify a choice
already made for other reasons.

## 4. What it changes

For an owner managing a real property portfolio over a multi-decade horizon, the practical
implication is that the choice of building-data platform is a decision about where control
sits fifty years from now, not only about which features are available today. A subscription
lapse, an acquisition, or a vendor's business failure disrupts a cloud-authoritative
platform's usefulness immediately, because the authoritative record was never the owner's to
independently hold. An architecture built on open, published standards and stored as files
the owner controls has no equivalent single point of failure — the record remains usable
regardless of what happens to any vendor, because no vendor relationship is structurally
required to read it.

It also changes what "integration" means across the systems a real-estate owner actually
runs. Because the same underlying file structure can hold building data, lease records, and
financial records addressably in one place, achieving what would otherwise require licensing
and maintaining point-to-point integrations between three separate systems becomes a
property of the file structure itself — available specifically because no multi-tenant
commercial boundary sits between the record types.

## 5. Where this could be wrong

**Real-time, many-person collaborative editing is a genuine, stated weakness, not a
hypothetical one.** For fast-paced, synchronous design sessions with multiple people editing
the same element concurrently, a centrally-hosted platform with a live, arbitrated session
performs measurably better than the version-control-style merging this architecture uses.
This is a real trade accepted for offline-first operation, not a temporary gap expected to
close on its own.

**This architecture, as specified, does not scale to city-wide federation across buildings
under different ownership.** It is built for a portfolio under common ownership. Federating
a genuinely city-scale digital twin — potentially a million or more buildings under
heterogeneous ownership — would require a streaming and indexing layer this paper does not
specify and does not claim to provide.

**The evidence base is a single owner-operator's deployment, not a multi-site study.** The
architectural argument — that the five coupled properties of the commercial approach are
structural, not vendor-specific — is intended to generalize across the category, and the
underlying standards are, by definition, vendor-neutral. Whether the specific capability
claims hold at other portfolio sizes, other ownership structures, or other jurisdictions is
a real open question this single case does not resolve.

**Generative building-design tooling is, at the time of writing, closed and vendor-specific
across the industry.** Nothing in this architecture prevents a future generative-authoring
client from writing standard-compliant output directly into it, but no such capability is
claimed as delivered today.

## 6. Conclusion

The architecture shared across commercial cloud-based building-information platforms —
vendor-hosted data, subscription-gated access, lossy interoperability, per-seat pricing — is
one coupled design, not five independent choices, and the coupling that funds the vendor is
the same coupling that leaves an owner's long-run access to its own asset data at the
vendor's discretion. Moving the authoritative record to a directory of open-standard files
the owner holds outright breaks that coupling directly: it produces five real capabilities
the subscription-gated approach cannot provide by construction, at the honestly-stated cost
of weaker real-time collaborative editing. The case is not hypothetical — it restates a real
multi-building owner-operator's own internal reasoning, recorded before the substrate was
built, and it moves in the same direction as government building-procurement requirements in
several major jurisdictions, each of which specifies an open standard rather than a named
commercial product.

---

## 7. Claims and what would count against them

**Structural-capability claim.** At least four of the five capabilities identified in §2
(deed-portable record, offline field use, vendor-independent longevity, direct sensor
integration, cross-system data convergence) are unavailable to a representative
subscription-gated cloud platform by architectural construction — not merely by current
product configuration — such that no contractual or configuration change short of relocating
the authoritative data store would provide the capability.

**Regulatory-alignment claim.** Each of the government building-procurement frameworks
reviewed in §2 (US federal, UK, Singapore, Dubai) is satisfiable through open-standard
deliverables with no dependency on any single named commercial platform.

| Test | What it checks | Status |
|---|---|---|
| Offline-open verification | Files open correctly in an independent, standards-conformant viewer with no network connection and no active subscription | Verified in the current deployment |
| Cloud-platform offline behavior | A representative cloud-authoritative platform's read/write functionality with connectivity disabled | Not independently tested against a specific competitor product |
| Format-longevity check | Files produced under successive generations of the open standard remain readable in current open-source tooling with no data loss | Verified across two prior standard generations in the current deployment |
| Regulatory-conformance check | Each reviewed framework's published requirements checked for any clause requiring a specific named commercial platform | Verified directly against each framework's published text; none names a platform |
| Cross-system convergence check | Whether a representative cloud-authoritative platform co-locates building, lease, and financial records inside one authoritative store without a separate licensed integration | Not independently tested against a specific competitor product |

The structural-capability claim is falsified if fewer than four of the five capabilities are
found to require relocating the authoritative store, or if a cloud-authoritative platform is
shown to provide the same capability through configuration or contract alone. The
regulatory-alignment claim is falsified if any reviewed framework is found to require a
named commercial platform rather than open-standard conformance generally.

### Appendix A — Format stack

IFC (authoritative geometry and semantics); a machine-checkable validation contract for what
a compliant model must contain; an open collaboration-issue format for coordination history;
a standard asset-handover spreadsheet format; per-element sidecar records for property sets,
sensor data, and work orders; a hash-addressed, content-verified object store for version
history; two regenerable visualization caches (3D and 2D). The authoritative state is the
building-data file plus its sidecars; the visualization formats carry no information the
source does not already contain.

## References

International Organization for Standardization. 2024. *ISO 16739-1 — Industry Foundation
Classes for data sharing in the construction and facility management industries.*

buildingSMART International. Information Delivery Specification (IDS) 1.0.

buildingSMART International. buildingSMART Data Dictionary (bSDD).

International Organization for Standardization. *ISO 19650 — Organization and digitization
of information about buildings and civil engineering works, including building information
modelling.*

buildingSMART International. 2023. *BIM Collaboration Format (BCF) 3.0 Specification.*

National Institute of Building Sciences. COBie — Construction Operations Building
Information Exchange.

World Wide Web Consortium. SVG 2 Recommendation.

Khronos Group. 2022. *ISO/IEC 12113 — glTF 2.0.*

General Services Administration. BIM Guide Series, U.S. Public Buildings Service.

U.S. Department of Veterans Affairs. BIM Standard.

UK BIM Framework, built on ISO 19650.

Singapore Building and Construction Authority. CORENET X e-submission framework.

IfcOpenShell open-source IFC toolkit documentation.

European Union Publications Office. European Union Public Licence (EUPL) 1.2.

---

## Contributors

Peter M. Woodfine, Jennifer M. Woodfine, and Mathew Woodfine are credited as founding
contributors to Woodfine's building-information-modeling research programme.

## How this paper was produced

This paper was prepared with AI assistance under human editorial direction; all analytical
claims and conclusions are the responsibility of the named institutional author.

## Disclosures

The architecture and case deployment described are this workspace's own engineering work
and internal reasoning, disclosed as such rather than as an independent third-party
evaluation. This paper contains forward-looking statements about future capability
development; such statements reflect current intentions and are subject to change without
notice.

## Data and reproducibility

The open standards cited in this paper are publicly available from buildingSMART
International and the International Organization for Standardization. The internal
design-response document referenced in §3 is an unpublished primary source authored by this
workspace and is reported as primary authorial testimony, not as an externally verifiable
citation.
