---
schema: woodfine-bim-registry-v1
type: tiles-registry
status: draft-v1
updated: 2026-06-09
source: PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Combinations.pdf (V1, Jan 6 2026)
        CONSTRUCTION_MCorp_2026_01_06_Tiles_Leasing Plan Efficiencies_FIN.docx
        PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Alternatives.pdf
        inputs/Sketches/* (zone dimensions, V3 Jan 2026)
note: "Tile sizes TBD until Floor Plate dimensions are confirmed by architect.
       Availability percentages are for the Tile slot within its Floor Plate column."
---

# Tiles Registry

**Deliverable 2 — BIM Objects system.**

A **Tile** is the combination-layer BIM Object that sits between a Key Plan and a
Floor Plate. A Tile is one leasable block on a floor; it is composed of Key Plans of
the same category arranged side-by-side. The Floor Plate is built from one or more
Tiles plus a Building Core.

---

## Tile algebra

Three Tile types are defined in the V1 combination document. In the formulas below:

- `n`, `p`, `q`, `r` are unit counts (non-negative integers)
- `P_Small`, `P_Medium`, `P_Large` denote Corporate Office Key Plans sized as
  proportions of the Floor Plate (dimensions TBD from architect)
- `PO_Small`, `PO_Medium`, `PO_Large` denote Private Office Key Plans
  (PO-1 / PO-2 / PO-3 as defined in key-plans-registry.md)
- `P_Academic`, `P_Lab`, `P_Medical`, `P_Business`, `P_Civic` denote
  Professional Office Key Plans (A-1/2/3, L-1/2/3, M-1/2/3, B-1/2/3, C-1/2/3)

### T_Basic — Corporate Office Tile

```
T_Basic = n(P_Small) + p(P_Medium) + q(P_Large)
```

Pure Corporate Office composition. One climate zone per Tile. No Professional tenants.
`T_Basic` occupies the same slot as `T_Compound` in the Floor Plate column.

### T_Compound — Mixed Corporate Office Tile

```
T_Compound = n(P_Small) + p(P_Medium) + q(P_Large)
           + r(P_Academic + P_Lab + P_Medical + P_Business + P_Civic)
```

Mixed Corporate + Professional Office. One or more Professional Key Plans are
inserted into the column alongside Corporate Key Plans. The total leasable area
of `T_Compound` equals that of `T_Basic` for the same Floor Plate.

### T_Special — Private Office + Professional Tile

```
T_Special = n(PO_Small) + p(PO_Medium) + q(PO_Large)
           + r(P_Academic + P_Lab + P_Medical + P_Business + P_Civic)
```

Mixed Private Office (PO-1/2/3) + Professional Office. Used when the leasing plan
calls for individual office suites alongside specialty tenants.

---

## Floor Plate composition rule

```
Floor Plate = T_Basic | T_Compound | T_Special
            + Building Core
```

One Tile type occupies each leasable column of the floor. Multiple Tile types may
appear on the same floor (one per column). Building Core (stairs, elevators, MEP)
is not part of any Tile.

### Development class targets

| Class | Floors | Floor plate | Tile columns | Key Plans = Climate Zone? |
|---|---|---|---|---|
| Professional Centres | 3–5 | 19,000–23,000 SF | 2–4 | No |
| Suburban Office | 6–9 | 17,000–21,000 SF | 2–3 | No |
| Retail Select | — | = Tile area | 1 | Yes |
| Tech Industrial | — | = Tile area | 1 | Yes |

For Retail Select and Tech Industrial, the Floor Plate equals the Tile area directly;
Key Plans define the climate zone and there is no separate Tile-composition layer.

---

## Tile slot availability (Professional Office categories)

When a T_Compound or T_Special Tile includes a Professional Key Plan slot, the
available size mix is:

| Category | Small | Medium | Large |
|---|---|---|---|
| Medical | 40% | 40% | 20% |
| Business | 20% | 60% | 20% |
| Laboratory | 40% | 40% | 20% |
| Academic | 20% | 60% | 20% |
| Civic | 20% | 60% | 20% |

These percentages describe the expected distribution across a project, not a per-Tile
constraint. A single Tile may hold any one size.

---

## WELL compliance note

All Key Plans used in Professional Office Tiles must support tenant compliance with
WELL Building Standard requirements. Source: handwritten annotation on multiple sketch
PDFs (V10, Medical / Business / Academic / Civic series). Zone widths in
key-plans-registry.md are sized to accommodate the circulation paths and daylighting
depths required by WELL. No Tile composition should override or reduce Zone 1 depth.

---

## 1. Professional Centres Tiles

Floor Plate: 19,000–23,000 SF. 3–5 storeys. All three Tile types apply.
Corporate Key Plan sizes are proportional to the floor; exact dimensions are
architect-gated until Floor Plate geometry is confirmed.

| Tile code | Type | Corporate slots | Professional slot | Notes |
|---|---|---|---|---|
| TC-BASIC | T_Basic | 2× P_Medium + n× P_Small | — | Full Corporate floor |
| TC-COMPOUND-M | T_Compound | 1× P_Medium + n× P_Small | 1× Medical (any size) | Medical inclusion |
| TC-COMPOUND-B | T_Compound | 1× P_Medium + n× P_Small | 1× Business (any size) | Business inclusion |
| TC-COMPOUND-L | T_Compound | 1× P_Medium + n× P_Small | 1× Laboratory (any size) | Laboratory inclusion |
| TC-COMPOUND-A | T_Compound | 1× P_Medium + n× P_Small | 1× Academic (any size) | Academic inclusion |
| TC-COMPOUND-C | T_Compound | 1× P_Medium + n× P_Small | 1× Civic (any size) | Civic inclusion |
| TC-SPECIAL-M | T_Special | n× PO_Medium + p× PO_Small | 1× Medical (any size) | PO + Medical |
| TC-SPECIAL-B | T_Special | n× PO_Medium + p× PO_Small | 1× Business (any size) | PO + Business |
| TC-SPECIAL-L | T_Special | n× PO_Medium + p× PO_Small | 1× Laboratory (any size) | PO + Laboratory |
| TC-SPECIAL-A | T_Special | n× PO_Medium + p× PO_Small | 1× Academic (any size) | PO + Academic |
| TC-SPECIAL-C | T_Special | n× PO_Medium + p× PO_Small | 1× Civic (any size) | PO + Civic |

---

## 2. Suburban Office Tiles

Floor Plate: 17,000–21,000 SF. 6–9 storeys. Same Tile types as Professional
Centres; smaller floor plate reduces the column count by one.

| Tile code | Type | Notes |
|---|---|---|
| TS-BASIC | T_Basic | Full Corporate floor; fewer columns than TC series |
| TS-COMPOUND-* | T_Compound | Same Professional inclusion logic as TC series |
| TS-SPECIAL-* | T_Special | Same PO + Professional logic as TC series |

Exact column compositions are TBD pending Floor Plate geometry confirmation.

---

## 3. Retail Select and Tech Industrial

For these development classes, the Floor Plate equals the Tile area. A Key Plan
defines the climate zone of the entire floor. No separate Tile algebra applies.

| Tile code | Equivalent to | Notes |
|---|---|---|
| TR-KP-<code> | Key Plan <code> | e.g. TR-KP-M-2 = one Medical Medium Key Plan |
| TI-KP-<code> | Key Plan <code> | e.g. TI-KP-L-1 = one Laboratory Small Key Plan |

---

## Pending

The following items are TBD pending architect confirmation:

| Item | Blocker |
|---|---|
| Corporate Office Key Plan sizes (P_Small / P_Medium / P_Large m² values) | Floor Plate geometry not yet confirmed |
| T_Basic and T_Compound exact slot counts per development class | Follows from Corporate KP sizes |
| Tile IFC file generation (tile-*.ifc) | Deferred until tiles-registry is ratified |
| Building Core area and dimensions | Architect-gated; not a Tile component |
| Leasing Plan Efficiencies ratios | In CONSTRUCTION_MCorp_2026_01_06_Tiles docx — not yet processed |

---

## Source traceability

| Claim | Source |
|---|---|
| T_Basic / T_Compound / T_Special algebra | PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Combinations.pdf §1 |
| Floor Plate SF targets | PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Combinations.pdf §2 |
| Retail Select / Tech Industrial rule | PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Combinations.pdf §3 |
| Availability percentages | PROJECTS_MCorp_Tear Sheet_Floor Plates_Tiles_Combinations.pdf §4 |
| WELL annotation | Handwritten note, multiple Sketch PDFs (Medical, Business, Academic, Civic, V10) |
| Zone dimensions | inputs/Sketches — DISCOVERY_MCorp_Sketches_Key Plans_Summary.pdf (V3, Jan 2026) |
