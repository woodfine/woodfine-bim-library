---
display_name: Building Grid
section: Compositions
ifc_anchor: IfcGrid
uniclass: —
ifc_hierarchy: IfcRoot → IfcObjectDefinition → IfcObject → IfcProduct → IfcGrid
elements: Structural Module (1.524m/5ft) · Façade/Demising/Corridor Wall Thickness · Green/Yellow/Red Tolerance Bands
card_desc: Structural module, wall thicknesses, and floor-plate-width tolerance bands driving bidirectional adjustment
property_sets:
---
Structural module dimensions, wall and partition thicknesses, and the floor-plate-width tolerance bands (Green ±2.5ft, Yellow ±5ft, Red ±10ft) that drive tool-buildingwidth's bidirectional adjustment logic — what happens when a target floor plate width doesn't land exactly on the Zone 1/2/3 arithmetic. Zone 1 Habitat and Zone 3 Corridor are locked by regulatory minima; Zone 2 Magazine is the only zone with no hard floor and yields first. See also Building Width Calculator for the zone-depth tokens these tolerances apply to.
