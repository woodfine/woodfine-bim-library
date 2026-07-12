## What is a BIM Object?

A BIM Object is a smart specification for one part of a building. Geometry, product data, and the rules it must meet — carried together in one open file that travels with the part through every tool that touches it.

When an architect places a wall, the wall's BIM Object already knows its required fire rating, its thermal transmittance range, and which code clause governs it in this jurisdiction. The compliance constraint is encoded in the starting material — no post-hoc checking, no separate specification document to fall out of date.

Every Object answers three questions:

1. **What is it?** — its formal identity: IFC 4.3 entity anchor, Uniclass 2015 classification, property sets.
2. **What must it meet?** — regulatory overlays: building-code clauses, fire ratings, energy standards, registered against the element type.
3. **Where does it work?** — climate-zone performance requirements that change with geography (ASHRAE, NBC 2020).

### Under the hood — the data model

Each BIM Object is stored as W3C Design Token Community Group (DTCG) format JSON — an open, text-diffable format with no proprietary container. Standards backbone: IFC 4.3 (ISO 16739-1:2024), Uniclass 2015, IDS 1.0, bSDD.

## The containment model

An Object — a desk, a luminaire, a door — is a physical part. A Key Plan, a Tile, a Floor Plate, a Building is a volume of space. The Library keeps these two categories strictly separate, because confusing them is the single most common category error in BIM data modelling: a wall is not a room, and a room is not a wall, even though both are things a building is "made of." IFC 4.3 makes the same distinction structurally — an `IfcFurniture` and an `IfcSpace` are fundamentally different kinds of entity, joined by an "is located in" relationship, not a "is part of" one.

**Objects don't aggregate upward.** An Object is a standalone part; it never sums into something larger the way a Key Plan sums into a Tile. Every Object placed in a Key Plan is listed on that Key Plan's **parts list** — a record of what the room contains, not a new rung above the Object itself.

**Key Plans, Tiles, and Floor Plates aggregate — but not by simple addition.** A Tile is not Key Plans summed together, and a Floor Plate is not Tiles summed together. Each scale nests into the one above it without remainder, the same self-similar arrangement repeating from a single Key Plan up to the whole building.

**The two categories meet by containment, not aggregation.** An Object is *placed inside* a Key Plan — the desk sits in the room, but the desk is not "part of" the room the way the room is part of the floor above it.

## Key Plans and Tiles

We plan space from the furniture out, not the square footage down. A **Key Plan** is the smallest unit of space worth leasing: a bounded room-scale plan defined by real furniture placement, real circulation, and real daylight — not by an area quota. Key Plans combine into **Tiles**: blocks of Key Plans that serve double duty as the unit a tenant leases and the zone the building's services and climate systems serve. Tiles combine into **Floor Plates** — and a floor plate assembled this way arrives with its light, circulation, and ventilation already proven at every scale below it. This fractional, self-similar composability — an eighth, a quarter, a half, three-quarters, or a full floor plate — is our own extension of the space ladder. Key Plan is real drafting terminology, though it conventionally names a small-scale locator diagram rather than a leasable room-scale unit; Tile has no single standard AEC equivalent, the closest familiar concepts being a structural bay, a planning module, a demise, or an HVAC zone — both are our own operationalization, in the same sense as Habitat, Magazine, and Corridor below. We currently publish six leasable Key Plan categories — Private Office, Medical, Business, Laboratory, Academic, Civic; Amenity and Common Area categories are in active design and not yet published.

Every Key Plan resolves into three parts. **Habitat:** where people work, held within six metres of the building perimeter so every workstation gets natural light. **Magazine:** storage and flexible depth — the dimension you can only find by iterating real plans, not by formula. **Corridor:** circulation, sized by its own Key Plan. Habitat and Magazine mirror each other across Corridor. The building's width is not assumed; it is computed outward from these three parts. The underlying logic — a daylight-adjacent zone, a flexible interior zone, and a circulation zone — is a well-established principle in building science and space planning generally (ASHRAE perimeter-zone HVAC guidance, the British Council for Offices' Guide to Specification, LEED and WELL daylight-zone requirements). Habitat, Magazine, and Corridor, and their coupling to the Building Width Calculator below, are our own operationalization of that principle. We also design every Key Plan so a tenant can meet its own WELL certification requirements directly from the geometry — light, air, and circulation proven at the room scale, not assumed and checked later.

The efficiency claim is specific: a plan built from real furniture and circulation wastes less area than a plan built from a square-footage formula. Waste less area per tenant and you can build less total floor area while housing the same number of tenants — what that means for the Library's larger sustainability argument is developed in Geometry of Sustainability, below.

The Key Plans are intended to carry 70–80% of building-certification requirements on their face — circulation, natural light, and ventilation are visible in the geometry itself, rather than assembled after the fact for an audit.

A Key Plan's constituent-Objects view is its **parts list** — every Object placed in that Key Plan. See "The containment model" above for why that relationship is containment, not composition.

### The formal definition

We define "Key Plans and Tiles" as a geometric self-similar aperiodic space planning system, based on furniture and equipment arrangements and circulation, rather than a modular area-per-person progression. In plain terms: the same pattern repeats at every scale (self-similar), it does not repeat on a fixed grid (aperiodic), and its size comes from real furniture and circulation, not a formula applied per person or per square foot.

Key Plans nest into Tiles and Floor Plates without remainder, in both directions.

## Geometry of Sustainability

**Build less. Prove it first.**

The most consequential sustainability decision in any building is made before design begins: how much building to build. Every square metre that goes up must be manufactured, transported, assembled, conditioned for decades, and eventually taken apart. An efficient building that is larger than it needed to be is still a net loss against a smaller one — no operational saving repays floor area that should never have existed. We call this the reduction of the production curve — a sincere form of sustainability: less construction demanded from the world for the same accommodation delivered.

What makes building less possible is not restraint but proof. Buildings are oversized because of uncertainty — an area formula pads every room, because nobody knows at planning time whether the real furniture, the real circulation, the real daylight will fit. The Key Plan removes that uncertainty at the smallest unit of space worth leasing. Each one is drawn from actual furniture placement, actual circulation, actual daylight, resolving into the same three parts described above — Habitat, Magazine, Corridor — so that light, air, and movement are not commitments checked at audit time; they are visible in the plan itself.

Because a Tile is proven Key Plans and a Floor Plate is proven Tiles, that confidence survives aggregation. A building composed this way can be exactly as large as its accommodation requires — no padding for doubt. This is the first pillar of the Geometry of Sustainability, and it is why it comes first: efficiency improves the building you construct; the geometry decides how much building there is to improve.

The other two pillars work the same way at a different scale: landscape (the parking lot reprogrammed as a Forest Garden) and materials (selected from the start for adaptive reuse and urban mining). Each pillar is measurable. None is aspirational.

## Standards

- **IFC 4.3** (ISO 16739-1:2024) — entity backbone
- **Uniclass 2015** — classification floor
- **IDS 1.0** — regulatory overlay constraint format
- **bSDD** (buildingSMART Data Dictionary) — URI authority
- **DTCG** — W3C Design Token Community Group token format
