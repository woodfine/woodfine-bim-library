---
schema: journal-v2
slug: site-context-overlays
title: "Separating a Building Design From the Rules That Govern Where It Sits"
subtitle: "A data architecture that lets one reusable design carry a different, automatically computed compliance status in every jurisdiction it is proposed"
site: bim.woodfinegroup.com
imprint: WCP-2026-06
thesis: "Building-code and site-environmental data are conventionally authored as a one-off prose report tied to a single project; separating the reusable design from the place-specific rules that govern it, and computing compliance as a derived result rather than authoring it as a verdict, lets the same design travel across jurisdictions without being re-authored or re-verified from scratch each time."
abstract: |
  An architect who has designed a compliant stairwell or a well-configured office on one
  project effectively starts from a blank sheet on the next, even in the same jurisdiction and
  even for the same kind of space, because the code-compliance conclusion was never recorded
  as reusable data — it was written up as a prose report tied to that one project. We describe
  an architecture that keeps three things structurally separate: a reusable functional-space
  design that is jurisdiction-agnostic by construction; a place-specific overlay holding the
  regulatory rules and environmental facts that apply at a given location; and a compliance
  result, which is always computed from the pairing of the two and never hand-authored or
  stored as a standalone verdict. Under this architecture, registering a newly-supported
  jurisdiction requires exactly one new overlay record and zero edits to any existing design.
  We specify a closed, four-category schema organizing the kinds of place-specific data a
  design actually needs — legal requirements, hazard and structural loads, long-run climate
  averages, and site-specific ground conditions — and a self-hosted model that lets a
  practitioner build and keep a private, portable library of reusable designs across an entire
  career without depending on a centrally hosted account system. We ground our internal
  terminology directly in the published open building-data standard's own existing
  distinction between a physical building element and a volume of space, correcting an
  earlier internal description that had incorrectly treated the two as the same kind of
  thing. The architecture is specified and partially implemented; a full-scale usability test
  against a practitioner's real, career-length design library has not yet been run.
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
  - ifc-fragment-spec
  - corenet-x-2021
  - ashrae-90-1
  - bco-guide-to-specification
  - well-v2-daylight-modeling
  - eupl-1-2
draws_from:
  - flat-file-bim-substrate
  - aec-data-layers
  - bim-object-specification
contributors:
  - name: Peter M. Woodfine
    roles: [Founding Contributor]
  - name: Jennifer M. Woodfine
    roles: [Founding Contributor]
  - name: Mathew Woodfine
    roles: [Founding Contributor]
keywords:
  - jurisdiction-portable design
  - regulatory compliance automation
  - building data standards
  - reusable design libraries
  - site context data
---

## 1. The question

An architect who has already designed a compliant emergency stairwell, a functional private
office, or a well-configured service room on one project starts the next project from a
blank sheet, even when the new project sits in the same jurisdiction and calls for the exact
same kind of space — because the compliance conclusion from the first project was never
recorded as reusable data. It was written up as a prose consultant's report tied to that one
project, with no structure that would let a future project simply ask "has this design
already been verified here, or somewhere close enough to matter?" This is not a failure of
individual practice. It follows directly from how building-code and site-environmental
information is conventionally packaged — as a project-specific narrative document, not as
data attached to a reusable design artifact that can travel with that design to the next
project.

This paper asks a specific, testable question: can the regulatory and environmental facts
that govern a location be authored exactly once per jurisdiction, and applied automatically
to any number of reusable designs deployed there — including a practitioner's own personal
library of past designs, reused independently across an entire career — without editing
either the design or the jurisdiction's data every time a new pairing occurs?

## 2. What we found

**Separating the reusable design from the place-specific rule set, and computing compliance
rather than authoring it, removes the re-authoring problem by construction rather than by
discipline.** A reusable functional-space design stores only jurisdiction-neutral measured
facts — a clearance distance in meters, not a pass/fail threshold and not a named
jurisdiction's law. A place-specific overlay, scoped to one jurisdiction or location, holds
both the pass/fail regulatory rules and separately, the purely informational environmental
facts — a climate value, a seismic figure, a flood designation — that apply there. The
compliance result for a given design at a given place is always computed fresh from that
pairing, never hand-typed and never stored as a standalone conclusion. The same reusable
design can be simultaneously compliant against one jurisdiction's rules and non-compliant
against another's, and this is not treated as a contradiction, because the design's own
definition never changed — only the place it was evaluated against did.

**The handful of cases where a regulatory difference is a genuine geometry difference — not
just a different pass/fail threshold — are handled by a substitution mechanism rather than
by mutating the base design.** A fire door required to be physically wider in one place than
another is not modeled as a jurisdiction field that changes the base design; instead the
design defines an open substitution slot, and the specific place being evaluated determines
which concrete variant fills that slot. Where no compliant variant is yet registered for a
given place, the system surfaces that gap explicitly rather than silently defaulting to a
possibly non-compliant choice.

**The place-specific data a design needs clusters cleanly into exactly four categories, and
the grouping principle is what each layer measures, not whether it happens to be a law.**
Most usable place-specific facts are code-referenced somewhere, so sorting them by "is this a
legal requirement" does not cleanly separate them. Sorting instead by what kind of question
each layer answers — a legal rule, a return-period extreme event, a long-run climate average,
or an in-situ physical site property — produces four categories that hold up cleanly:
regulatory and entitlement rules; hazard and structural-load extremes; climate and energy
averages; and ground and ecological conditions. Interactions between categories — a seismic
figure amplified by local soil conditions, a flood designation that is simultaneously a
physical hazard and a trigger for a separate regulatory requirement — are resolved at
compliance-computation time, not by duplicating a layer's data into two categories.

**A terminology correction, made explicit rather than quietly folded in, matters for
credibility with anyone literate in the underlying open standard.** An earlier internal
description of this architecture's spatial hierarchy — small unit, grouping of units, floor,
building — described the smallest unit as itself "a building element," conflating the open
standard's own physical-element hierarchy (walls, doors, furniture) with its separate
spatial-volume hierarchy (a room, a zone, a storey). The two hierarchies converge only at a
shared, more abstract level in the standard, and conflating them lower down is a real
category error we found, corrected, and report explicitly rather than silently fixing.

## 3. How we built it

The architecture defines three deliberately independent record types. A **design** is a
jurisdiction-agnostic functional-space specification — a reusable room or assembly type —
storing only jurisdiction-neutral measured facts, never a verdict. A **place overlay** is
scoped to a jurisdiction or location and holds two kinds of content under one mechanism:
pass/fail regulatory requirements, each citing its actual source, and purely informational
environmental facts; both attach to a design or an individual element by classification code
rather than by editing the target record directly. A **compliance result** is a computed,
cacheable outcome for one design-and-overlay pairing — never hand-authored, always
re-derivable from the pairing that produced it.

The place-specific data itself is organized under a closed, four-value category schema —
regulatory and entitlement rules, hazard and structural-load extremes, climate and energy
averages, and ground and ecology conditions — while the individual data layers within each
category remain an open, extensible vocabulary. The specific per-country data sources and
their licensing status are a separate research effort in their own right, referenced here as
related work rather than re-derived; this paper's own finding is narrower — that the layers
cluster cleanly into these four categories regardless of which specific national source
ultimately populates each one.

We corrected our own internal spatial-hierarchy terminology against the open building-data
standard's actual published schema, distinguishing physical elements (a door, a piece of
furniture) from spatial volumes (a room, a zone, a floor, a building) and distinguishing true
whole-part decomposition (a floor group made up of smaller units) from mere physical
containment (furniture located inside a room, not decomposed into it). Both hierarchies
converge only at a shared, more abstract supertype in the standard — the level at which
everything is placeable and classifiable — not at the level of an individual physical
element. A self-similar, fractional grouping mechanism we use for subdividing a floor
(quarter, half, three-quarter, full) is our own extension layered on top of the standard's
spatial-grouping concept, not a feature the standard itself defines, and we say so directly
rather than presenting it as a standard feature.

Ownership follows a self-hosted model rather than a centrally hosted account system: a
practitioner runs their own instance of the underlying open-source platform, with a fully
private, offline, local-network-only deployment as a first-class supported mode, not a
degraded fallback. A practitioner's own accumulated design library — potentially hundreds of
designs spanning an entire career — registers as an extension layered on a shared base
catalogue, pulling in base-catalogue updates while keeping the practitioner's own designs
private and under their own governance.

## 4. What it changes

For a design practice, the practical change is that registering support for a new
jurisdiction becomes a single new record addition with zero edits to any existing design —
rather than a re-verification exercise repeated from scratch for every design that might be
proposed there. This is the architectural property that makes real reuse possible at all:
the re-authoring problem this paper opened with is closed by how the data is structured, not
by relying on a practitioner's discipline in keeping records straight across dozens of
projects and jurisdictions.

It also changes what a practitioner's own accumulated body of work is worth over time. A
personal library of past designs — a stairwell detail used on an unrelated project years
earlier, in a different jurisdiction — becomes something a practitioner can locate and
directly reuse, fully evaluated for compliance at the new location automatically, rather than
something that exists only as an unindexed archive of old project files.

## 5. Where this could be wrong

**The four-category schema is validated by internal consistency, not by an outside survey of
how practitioners actually think about classifying site data.** Whether architects and
engineers outside this specific effort would independently arrive at the same four
categories, rather than a different grouping that also happens to be internally coherent, is
untested.

**The self-hosted library model has not yet been evaluated at the scale its own value
proposition describes.** The claimed benefit — fast, relevant retrieval from a personal
library of hundreds of designs spanning a career — has not been measured against a real
practitioner's library at that scale; it remains a design goal, not a demonstrated result.

**The corrected spatial-hierarchy terminology has been checked against the published
standard's own schema documentation, but not yet reviewed by an outside practitioner fluent
in that standard.** The correction rests on an internal architectural review, not external
validation by someone with no stake in the original framing.

**The specific three-zone floor-planning package this platform uses is our own
operationalization of a well-established general principle (organizing floor depth from the
facade inward for daylight, flexibility, and circulation), not itself a citation to existing
external practice under those specific names.** We state this distinction directly rather
than implying the specific package is an industry-standard term already in use elsewhere.

## 6. Conclusion

The re-authoring problem this paper opened with — an architect rebuilding the same kind of
space, and re-verifying its compliance from scratch, on every project — is not a discipline
problem solvable by better habits; it is a direct consequence of packaging code and site data
as a one-off prose report instead of as structured, reusable data. Separating the reusable
design from the place-specific overlay, and deriving compliance as a computed result rather
than authoring it as a stored verdict, removes the problem by construction: a design
authored once is deployable anywhere, registering a new jurisdiction adds one record and
edits nothing existing, and the same design carries a different, automatically-derived
compliance status wherever it is proposed. The architecture is specified and running in a
real deployment; a full-scale test against a practitioner's actual career-length design
library — the scenario the whole approach is built to serve — has not yet been run.

---

## 7. Claims and what would count against them

**Zero-edit onboarding claim.** Registering a new jurisdiction's place overlay requires zero
edits to any existing design record — only a new overlay record and, where a genuine
geometric variation exists, a new substitution-slot resolution.

**Terminology-mapping claim.** The corrected spatial-hierarchy model maps every internal
term to a distinct concept in the published open building-data standard, with no internal
term mapped to more than one standard concept and no standard concept required to represent
two different internal terms.

| Test | What it checks | Status |
|---|---|---|
| Zero-edit jurisdiction onboarding | Authoring a new place overlay for an existing design already deployed elsewhere requires no edit to the design itself | Verified in the current implementation |
| Simultaneous divergent compliance | The same design can be represented as compliant against one overlay and non-compliant against another without duplicating the design record | Verified in the current implementation |
| Standard-mapping completeness | Every internal term maps to exactly one distinct concept in the published standard's schema documentation | Checked directly against the published schema; holds for all mapped terms |
| Practitioner-library scale test | Retrieval speed and relevance for a personal library of 100+ designs spanning multiple jurisdictions, against the same interface used for the shared base catalogue | Not yet run — no practitioner library at this scale has been tested |

The zero-edit onboarding claim is falsified if authoring a new overlay is found to require
editing an existing design record. The terminology-mapping claim is falsified if any
internal term is found to map to more than one standard concept, or if two internal terms
are found to require the same standard concept.

### Appendix A — The four-category schema

Regulatory and Entitlement (what law requires at this location — pass/fail); Hazards and
Structural Loads (what extreme event the structure must survive — return-period figures);
Climate and Energy (long-run environmental averages); Ground and Ecology (what the site
itself physically contains — measured in-situ properties). Cross-category interactions are
resolved at compliance-computation time rather than by duplicating a layer into two
categories.

## References

buildingSMART International. *Industry Foundation Classes 4.3 — spatial structure and
element schema.*

buildingSMART International. Information Delivery Specification (IDS) 1.0.

buildingSMART International. buildingSMART Data Dictionary (bSDD).

Singapore Building and Construction Authority. CORENET X e-submission framework.

ASHRAE. *Standard 90.1 — Energy Standard for Buildings*, perimeter-zone HVAC modeling
guidance.

British Council for Offices. *Guide to Specification*, daylight/ventilation perimeter-zone
and services-core-zone guidance.

International WELL Building Institute. *WELL Building Standard v2*, daylight-modeling
feature.

European Union Publications Office. European Union Public Licence (EUPL) 1.2.

---

## Contributors

Peter M. Woodfine, Jennifer M. Woodfine, and Mathew Woodfine are credited as founding
contributors to Woodfine's building-information-modeling research programme.

## How this paper was produced

This paper was prepared with AI assistance under human editorial direction; all analytical
claims and conclusions are the responsibility of the named institutional author.

## Disclosures

The architecture and implementation described are this workspace's own engineering work.
This paper contains forward-looking statements about a planned practitioner-scale evaluation;
such statements reflect current intentions and are subject to change without notice.

## Data and reproducibility

The open standards cited in this paper are publicly available from buildingSMART
International. The internal design-response document informing the terminology correction in
§3 is an unpublished primary source authored by this workspace and reported as primary
authorial testimony, not as an externally verifiable citation. Per-jurisdiction data-layer
sourcing is documented in a related paper (`aec-data-layers`), cited here as related work
rather than re-derived.
