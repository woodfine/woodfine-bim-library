# AEC muscle-memory rationale

Every architect, engineer, construction manager, and property
manager who opens a new BIM authoring tool for the first time carries
a learned interface vocabulary from Revit, ArchiCAD, BricsCAD, or
Bonsai (the open-source IFC authoring tool, formerly BlenderBIM). The
Building Design System adopts that vocabulary by default. Learning
is reserved for the parts of the substrate that are genuinely new:
the flat-file vault, the City Code as Composable Geometry overlay,
and the BIM + lease register + financial ledger convergence.

## Universal AEC interface conventions

A cross-walk of production BIM tools identified ten components that
converge across all of them:

1. **Spatial tree** — left rail. Site / Building / Storey / Space
   hierarchy. Default-expand to storey level (a Bonsai convention) —
   never auto-expand into individual spaces.
2. **Properties panel** — right rail. Property and quantity sets for
   the selected element, with an editable variant for authoring
   contexts and a read-only variant for operational/viewing contexts.
3. **3D viewport** — main canvas, with an embedded web-based IFC
   viewer. Selection synchronises bidirectionally with the spatial
   tree.
4. **View navigator** — saved views as tabs (a Bonsai convention).
5. **Toolbar** — top of viewport. Tool selection (select / measure /
   section plane / annotation / BCF capture).
6. **Status bar** — bottom of viewport. Camera coordinates, current
   selection, edit-mode indicator.
7. **Selection filter** — element-class filter (show only walls,
   only spaces, etc.).
8. **Type browser** — IFC type library browser; insertion of typed
   elements.
9. **Section plane** — section / plan / elevation generation and
   editing.
10. **Annotation layer** — text labels, leader lines, dimensions
    overlaid on the viewport.

These ten components are dual-mode by design: an authoring context
enables editing, an operational/viewing context disables editing
while preserving every other affordance.

## Surface-specific components

### Authoring-specific

- **Materials browser** — material library with classification-URI
  search and property-set editing.
- **Type editor** — IFC type library authoring (parametric type
  variations, e.g. a wall type with parameters for thickness and
  acoustic rating).
- **Clash detector** — geometric intersection detection across
  federated IFC files.
- **Version history** — a git-style diff over the vault's object and
  reference history.

### Operations-specific

- **GUID search** — primary entry point for facility-management
  operators. Search by IFC GUID, entity class, classification URI,
  or space name.
- **Audit log** — flat-file vault commit history rendered for
  facility-management operators (when did the boiler get replaced?
  which contractor? what spec?).
- **Dashboard** — element counts, vault size, last ingestion
  timestamp, operational metrics.
- **Export panel** — COBie CSV download, IFC re-export, and
  CityJSONSeq portfolio export.

## Workflows with no direct precedent in existing open-source tools

Open-source IFC authoring tools like Bonsai target the architect and
designer persona; the facility-management operator persona that
current authoring tools do not address needs its own workflows:

1. **Work-order linking** — attach a work order to an IFC element.
   The per-element sidecar carries the work-order identifier, status,
   and assignee. The element's history becomes a chronological work
   ledger.
2. **Lease linking** — attach a lease record to a space entity. The
   sidecar references the lease entity in the bookkeeping vault.
   Lease and space are co-versioned.
3. **Sensor overlay** — live sensor readings overlaid on the relevant
   element in the 3D viewport. Readings persist as timestamped data
   in the per-element sidecar.

These three workflows operationalise the convergence of BIM, lease
register, and financial ledger into one portable archive.

## What the Building Design System deliberately does not do

- **Modal mode-switching workflows.** Editor-style modal modes are
  invisible in purpose-built authoring tools. Not carried forward.
- **Numpad view-axis shortcuts.** Most laptops have no numpads. The
  convention used here is number keys 1-6 along the top row.
- **Outliner-as-spatial-tree.** Reusing a host application's generic
  object outliner as the spatial hierarchy view is a host-environment
  artifact, not a considered design decision — not carried forward. A
  purpose-built spatial tree widget is used instead.
- **Authoring-first operational views.** The operational/read-only
  surface is read-only by intent; the dual-mode contract enforces
  this rather than allowing it to be bypassed.
