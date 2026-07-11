---
display_name: Key Plans
section: Objects
ifc_anchor: IfcSpace
uniclass: SL_25
ifc_hierarchy: IfcRoot → IfcObjectDefinition → IfcObject → IfcSpatialElement → IfcSpace
elements: Private Office · Medical · Business · Laboratory · Academic · Civic · Corporate Office
card_desc: Leasable spatial programs with zone depths, furniture programs, and compliance data
property_sets: Pset_SpaceCommon,NetFloorArea,IfcAreaMeasure; Pset_SpaceCommon,IsExternal,BOOLEAN; Pset_OccupancyRequirements,OccupancyNumber,INTEGER
---
Key Plans — the smallest unit of space worth leasing, planned from the furniture out.

A Key Plan is a space, not a product — `IfcSpace` in the hierarchy above, the same category as a Tile or a Floor Plate, not the same category as an Object. It is the smallest spatial program worth leasing: real furniture placement, a three-zone cross-section (Zone 1 Habitat / Zone 2 Magazine / Zone 3 Corridor), net leasable area, and accessibility compliance. Authored by architects from Woodfine equipment programs; Key Plans nest into Tiles and Floor Plates without remainder, in both directions.
