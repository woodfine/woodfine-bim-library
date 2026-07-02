## What is a BIM Object?

A BIM Object is a machine-readable specification unit stored in W3C Design Token Community Group (DTCG) format JSON. Each object is anchored to an IFC 4.3 entity class and carries three layers of constraint data:

1. **Specification** — the IFC entity anchor, applicable Uniclass 2015 code, bSDD URI, and property set definitions.
2. **Regulation** — jurisdictional overlays (building code clauses, fire ratings, energy standards) registered against the element type.
3. **Climate Zone** — performance requirements that vary by geographic zone (ASHRAE, NBC 2020).

## Key Plans

Key Plans extend the BIM Object model to the spatial program layer. A Key Plan is the smallest leasable BIM Object: a bounded IfcSpace defined by real furniture placement, a three-zone cross-section (Zone 1 Habitat / Zone 2 Magazine / Zone 3 Corridor), net leasable area, and accessibility compliance.

Key Plans nest into Tiles (climate zone boundaries), which nest into Floor Plates (full building-floor programs). The tool-buildingwidth Rust engine computes remainder-free nesting in both directions.

## Standards

- **IFC 4.3** (ISO 16739-1:2024) — entity backbone
- **Uniclass 2015** — classification floor
- **IDS 1.0** — regulatory overlay constraint format
- **bSDD** (buildingSMART Data Dictionary) — URI authority
- **DTCG** — W3C Design Token Community Group token format
