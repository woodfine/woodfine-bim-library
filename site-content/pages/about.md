## What is a BIM Object?

A BIM Object is a smart specification for one part of a building. Geometry, product data, and the rules it must meet — carried together in one open file that travels with the part through every tool that touches it.

When an architect places a wall, the wall's BIM Object already knows its required fire rating, its thermal transmittance range, and which code clause governs it in this jurisdiction. The compliance constraint is encoded in the starting material — no post-hoc checking, no separate specification document to fall out of date.

Every Object answers three questions:

1. **What is it?** — its formal identity: IFC 4.3 entity anchor, Uniclass 2015 classification, property sets.
2. **What must it meet?** — regulatory overlays: building-code clauses, fire ratings, energy standards, registered against the element type.
3. **Where does it work?** — climate-zone performance requirements that change with geography (ASHRAE, NBC 2020).

### Under the hood — the data model

Each BIM Object is stored as W3C Design Token Community Group (DTCG) format JSON — an open, text-diffable format with no proprietary container. Standards backbone: IFC 4.3 (ISO 16739-1:2024), Uniclass 2015, IDS 1.0, bSDD.

## Two ladders, one substrate

Objects and Compositions are not the only structure in the Library — above them sits a second, parallel system: Key Plans, Tiles, and Floor Plates. The two are easy to conflate, but the distinction is load-bearing and the Library keeps them strictly separate.

**The parts ladder** holds physical things: an Object (a desk, a luminaire, a door) and a Composition (an Object assembly — a furnished room type). A Composition is built *from* Objects the way a piece of furniture is built from its components.

**The space ladder** holds volumes of space, not things: a Key Plan, a Tile, a Floor Plate, a Building. A Tile is built *from* Key Plans, and a Floor Plate is built *from* Tiles, the same way a building's storeys are built from rooms — this is composition-of-spaces, not composition-of-parts, and it follows its own, separate progression.

**The two ladders meet by containment, not aggregation.** A Composition is *placed inside* a Key Plan — the desk sits in the room, but the desk is not "part of" the room the way the room is part of the floor above it. Confusing these two relationships is the single most common category error in BIM data modelling: a wall is not a room, and a room is not a wall, even though both are things a building is "made of." The Library keeps them separate for the same reason IFC 4.3 does: an `IfcFurniture` and an `IfcSpace` are fundamentally different kinds of entity, joined by an "is located in" relationship, not a "is part of" one.

**What unifies them is one level up.** Both ladders converge only at the shared level of "a placeable, classifiable, thing" — every Object, Composition, Key Plan, Tile, and Floor Plate carries an identity, a classification, and a place in the model. That is the precise sense in which the catalog and the space-planning system are one data model, not two products: not because a Key Plan is a kind of Object, but because everything in the Library, on either ladder, is built the same way underneath.

## Key Plans and Tiles

Woodfine plans space from the furniture out, not the square footage down. A **Key Plan** is the smallest unit of space worth leasing: a bounded room-scale plan defined by real furniture placement, real circulation, and real daylight — not by an area quota. Key Plans combine into **Tiles**: blocks of Key Plans that serve double duty as the unit a tenant leases and the zone the building's services and climate systems serve. Tiles combine into **Floor Plates** — and a floor plate assembled this way arrives with its light, circulation, and ventilation already proven at every scale below it. This fractional, self-similar composability — an eighth, a quarter, a half, three-quarters, or a full floor plate — is Woodfine's own extension of the space ladder.

Every Key Plan resolves into three parts. **Habitat:** where people work, held within six metres of the building perimeter so every workstation gets natural light. **Magazine:** storage and flexible depth — the dimension you can only find by iterating real plans, not by formula. **Corridor:** circulation, sized by its own Key Plan. Habitat and Magazine mirror each other across Corridor. The building's width is not assumed; it is computed outward from these three parts. The underlying logic — a daylight-adjacent zone, a flexible interior zone, and a circulation zone — is a well-established principle in building science and space planning generally (ASHRAE perimeter-zone HVAC guidance, the British Council for Offices' Guide to Specification, LEED and WELL daylight-zone requirements). Habitat, Magazine, and Corridor, and their coupling to the Building Width Calculator below, are Woodfine's own operationalization of that principle.

The efficiency claim is specific: a plan built from real furniture and circulation wastes less area than a plan built from a square-footage formula. Waste less area per tenant and you can build less total floor area while housing the same number of tenants. Woodfine's source language calls this "the reduction of the production curve — a sincere form of sustainability" — less construction demanded from the world for the same accommodation delivered.

The Key Plans are intended to carry 70–80% of building-certification requirements on their face — circulation, natural light, and ventilation are visible in the geometry itself, rather than assembled after the fact for an audit.

A Composition's constituent-Objects view is its **parts list** — every Object that assembly is built from. A Composition, in turn, is *placed inside* a Key Plan, along with any other Compositions and standalone Objects the room contains — see "Two ladders, one substrate" above for why that relationship is containment, not composition.

### The formal definition

"Key Plans and Tiles" means a geometric self-similar aperiodic space planning system based on furniture/equipment arrangements and circulation versus modular area per person progressions. — Woodfine Openstudio design response

Key Plans nest into Tiles and Floor Plates without remainder, in both directions.

## Geometry of Sustainability

The space efficiency above — a plan sized by real furniture and circulation instead of an area formula — is the first of three measurable pillars in what Woodfine calls the Geometry of Sustainability: it is not a certification or a slogan, it is produced by the physical arrangement of things. The other two pillars work the same way at a different scale: landscape (the parking lot reprogrammed as a Forest Garden) and materials (selected from the start for adaptive reuse and urban mining). Each pillar is measurable. None is aspirational.

## Standards

- **IFC 4.3** (ISO 16739-1:2024) — entity backbone
- **Uniclass 2015** — classification floor
- **IDS 1.0** — regulatory overlay constraint format
- **bSDD** (buildingSMART Data Dictionary) — URI authority
- **DTCG** — W3C Design Token Community Group token format
