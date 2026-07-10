---
display_name: Interior
section: Objects
ifc_anchor: IfcFurniture
uniclass: —
ifc_hierarchy: IfcRoot → IfcObjectDefinition → IfcObject → IfcElement → IfcFurnishingElement → IfcFurniture
elements: IfcFurniture · IfcSystemFurnitureElement · circulation constraints
card_desc: Furniture BIM Objects and circulation constraints for Key Plan authoring
property_sets:
---
Interior — the furniture parts a Key Plan is authored from, and the circulation clearances each one demands.

Furniture BIM Objects and circulation constraints used to author Key Plans. Every furniture token carries confirmed manufacturer product data — dimensions, clearance, SKU, weight, IFC class, and source URL — sourced from Steelcase and Coalesse product pages. Circulation tokens carry the applicable accessibility code reference and spatial thresholds (ASR A1.2, DIN 18040, ArbStättV §12). Consumed by tool-keyplan for constraint validation and DTCG compilation.
