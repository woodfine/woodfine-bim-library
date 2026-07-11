---
display_name: Spatial
section: Taxonomy
ifc_anchor: IfcSpatialElement
uniclass: SL
ifc_hierarchy: IfcRoot → IfcObjectDefinition → IfcObject → IfcSpatialElement
elements: IfcSite · IfcBuilding · IfcBuildingStorey · IfcSpace
card_desc: Spaces, levels (IfcBuildingStorey), buildings, sites, and zones
property_sets: Pset_SpaceCommon,IsExternal,BOOLEAN; Pset_SpaceCommon,NetFloorArea,IfcAreaMeasure; Pset_BuildingCommon,NumberOfStoreys,INTEGER; Pset_SiteCommon,BuildableArea,IfcAreaMeasure
---
Spatial — the containers a building's spaces sit inside: sites, buildings, storeys, and zones.

Spatial elements define the hierarchy of a building's geography: site, building, storeys, and individual spaces. They are the containers that built elements occupy, and the entities that jurisdictional and climate zone constraints apply to at a zone level.
