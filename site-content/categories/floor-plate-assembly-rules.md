---
display_name: Floor Plate Assembly Rules
section: Compositions
ifc_anchor: IfcConstraint
uniclass: —
ifc_hierarchy: IfcRoot → IfcConstraint
elements: FP-SUM-001 · FP-ENDCAP-001 · FP-CORE-001 · FP-SNAP-001 · FP-CLIMATE-001 · FP-DOORS-001 · FP-CORNER-001
card_desc: Machine-readable validation rules for a valid floor plate composition
property_sets:
---
Floor Plate Assembly Rules — the machine-checked rules that decide whether a floor plate composition is valid.

Machine-readable validation rules (FP-*) for a valid floor plate composition — tile-area summation tolerances, end-cap and core placement constraints, HVAC climate-zone-per-tile, door counts, and corner-tile structural-grid review triggers. Previously these rules existed only as narrative text in PDFs; here they are stated as predicates a validator can actually evaluate. See also Tile System for the tiles these rules validate, and Building Grid for the tolerance bands referenced by several rules.
