#!/usr/bin/env python3
"""
Generate IFC4 Key Plan compositions for Private Office PO-1 / PO-2 / PO-3.

Each output file is a self-contained IFC4-SPF composition containing:
  - IfcSpace (room boundary with bounding-box geometry)
  - IfcFurniture instances placed at 2D plan coordinates
  - Pset_FurnitureTypeCommon property sets on each furniture item

Source: tokens/bim/key-plans.dtcg.json (private-office entries) and
        tokens/bim/interior.dtcg.json (furniture dimensions).

Output: key-plans/private-office-{1,2,3}.ifc

Usage: python3 scripts/generate-key-plans.py
"""

import uuid
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# IFC GUID helpers
# ---------------------------------------------------------------------------
_GUID_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"


def ifc_guid():
    n = uuid.uuid4().int
    result = []
    for _ in range(22):
        result.append(_GUID_CHARS[n % 64])
        n //= 64
    return "".join(reversed(result))


# ---------------------------------------------------------------------------
# Key Plan definitions (from tokens/bim/key-plans.dtcg.json)
# ---------------------------------------------------------------------------
KEY_PLANS = [
    {
        "code": "PO-1",
        "name": "Private Office — Small",
        "filename": "private-office-1.ifc",
        "area_m2": 30.19,
        "z1": 6.0,
        "z2": 3.8,
        "z3": 2.0,
        "size": "small",
    },
    {
        "code": "PO-2",
        "name": "Private Office — Medium",
        "filename": "private-office-2.ifc",
        "area_m2": 43.20,
        "z1": 6.0,
        "z2": 3.8,
        "z3": 2.0,
        "size": "medium",
    },
    {
        "code": "PO-3",
        "name": "Private Office — Large",
        "filename": "private-office-3.ifc",
        "area_m2": 63.64,
        "z1": 6.0,
        "z2": 3.8,
        "z3": 2.0,
        "size": "large",
    },
]

# Furniture dimensions in mm (from interior.dtcg.json); converted to metres for IFC
FURN_DIMS = {
    "desk":       {"w": 1.473, "d": 0.737, "h": 0.574},   # Migration SE 58x29
    "chair":      {"w": 0.686, "d": 0.629, "h": 0.978},   # Leap V2
    "table":      {"w": 0.914, "d": 0.914, "h": 0.724},   # Groupwork 36" (round)
    "credenza":   {"w": 1.830, "d": 0.457, "h": 0.737},   # Currency Credenza 72"
    "bookcase":   {"w": 0.914, "d": 0.381, "h": 1.846},   # Currency Bookcase 36"
    "pedestal":   {"w": 0.387, "d": 0.559, "h": 0.533},   # TS Mobile Pedestal
    "lounge":     {"w": 0.899, "d": 0.896, "h": 1.031},   # Wing Chair CH445
    "coat_rack":  {"w": 0.400, "d": 0.300, "h": 1.800},   # Generic Coat Rack
}

# Pset_FurnitureTypeCommon designations
FURN_PSET = {
    "desk":      ("Steelcase Migration SE Height-Adjustable Desk", "58\" x 29\" Rectangle"),
    "chair":     ("Steelcase Leap V2 Ergonomic Chair",            "Task Chair"),
    "table":     ("Steelcase Groupwork 36-Inch Round Table",      "Working Height Round Table"),
    "credenza":  ("Steelcase Currency Credenza 72\"",              "Credenza Storage"),
    "bookcase":  ("Steelcase Currency Bookcase 36\"",              "Upright Bookcase"),
    "pedestal":  ("Steelcase TS Mobile Pedestal",                  "Mobile Storage Pedestal"),
    "lounge":    ("Coalesse Wing Chair CH445",                     "Lounge Seating"),
    "coat_rack": ("Generic Coat Rack",                            "Freestanding Hook Panel"),
}


def furniture_layout(kp):
    """
    Return list of (furn_type, x, y) placement tuples for a given key plan.

    Coordinate origin: lower-left of Zone 3 (corridor end of room).
    X = width (frontage) axis.
    Y = depth axis: Zone 3 (0–z3), Zone 2 (z3–z3+z2), Zone 1 (z3+z2–total).
    All units: metres.
    """
    w = kp["area_m2"] / (kp["z1"] + kp["z2"] + kp["z3"])
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []

    # ── Zone 1 (facade) — desk + chair + table ──────────────────────────────
    # Desk against façade wall: centred left of space, 100 mm inset
    desk_x = 0.10
    desk_y = z1_start + 0.10
    items.append(("desk", desk_x, desk_y))

    # Task chair pulled forward from desk (desk depth + 0.2 m clearance)
    items.append(("chair", desk_x + (FURN_DIMS["desk"]["w"] - FURN_DIMS["chair"]["w"]) / 2,
                  desk_y + FURN_DIMS["desk"]["d"] + 0.20))

    # Mobile pedestal right of desk
    items.append(("pedestal", desk_x + FURN_DIMS["desk"]["w"] + 0.10, desk_y))

    # Round meeting table: placed centreward in Z1 depending on size
    if kp["size"] == "small":
        tbl_x = max(desk_x + FURN_DIMS["desk"]["w"] + 0.50, w / 2 - FURN_DIMS["table"]["w"] / 2)
        tbl_y = z1_start + kp["z1"] * 0.45
    elif kp["size"] == "medium":
        tbl_x = w / 2 - FURN_DIMS["table"]["w"] / 2
        tbl_y = z1_start + kp["z1"] * 0.40
    else:  # large
        tbl_x = w * 0.35
        tbl_y = z1_start + kp["z1"] * 0.38
    items.append(("table", tbl_x, tbl_y))

    # Lounge chair: large key plan only, against far wall
    if kp["size"] == "large":
        items.append(("lounge", w - FURN_DIMS["lounge"]["w"] - 0.10,
                      z1_start + kp["z1"] * 0.60))

    # ── Zone 2 (magazine) — credenza + bookcase ──────────────────────────────
    items.append(("credenza", 0.10, z2_start + 0.10))
    bookcase_x = min(0.10 + FURN_DIMS["credenza"]["w"] + 0.20,
                     w - FURN_DIMS["bookcase"]["w"] - 0.10)
    items.append(("bookcase", bookcase_x, z2_start + 0.10))

    # ── Zone 3 (corridor) — coat rack near door ──────────────────────────────
    items.append(("coat_rack", w - FURN_DIMS["coat_rack"]["w"] - 0.10, 0.10))

    return items, w


# ---------------------------------------------------------------------------
# IFC-SPF builder
# ---------------------------------------------------------------------------

def build_ifc(kp):
    """Return complete IFC4-SPF file content as a string."""
    depth = kp["z1"] + kp["z2"] + kp["z3"]
    items, width = furniture_layout(kp)
    area = kp["area_m2"]

    # Assign stable line-number IDs
    id_ = 10
    ids = {}

    def next_id():
        nonlocal id_
        v = id_
        id_ += 10
        return v

    lines = []

    # ── Header ───────────────────────────────────────────────────────────────
    lines.append("ISO-10303-21;")
    lines.append("HEADER;")
    kp_code = kp["code"]
    kp_name = kp["name"]
    kp_file = kp["filename"]
    lines.append(
        "FILE_DESCRIPTION(('IfcSpace Key Plan Composition — Woodfine BIM Library',"
        f"'KeyPlan:{kp_code}  {kp_name}'),'2;1');"
    )
    lines.append(
        f"FILE_NAME('{kp_file}','2026-06-03T00:00:00',"
        "(''),'','woodfine-bim-library generate-key-plans','','');"
    )
    lines.append("FILE_SCHEMA(('IFC4'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")

    # ── Shared geometry primitives ────────────────────────────────────────────
    ORIGIN    = next_id()
    AX3D_0    = next_id()
    GEOMCTX   = next_id()

    # ── Owner / application / units ──────────────────────────────────────────
    U_LEN     = next_id()
    U_AREA    = next_id()
    U_VOL     = next_id()
    UNITS     = next_id()
    PERSON    = next_id()
    ORG_WFP   = next_id()
    ORG_WBL   = next_id()
    PAO       = next_id()
    APP       = next_id()
    OWNHIST   = next_id()
    PROJ      = next_id()

    # ── Spatial hierarchy ────────────────────────────────────────────────────
    SITE_PL   = next_id()
    SITE      = next_id()
    BLDG_PL   = next_id()
    BLDG      = next_id()
    STOREY_PL = next_id()
    STOREY    = next_id()

    # ── Space ────────────────────────────────────────────────────────────────
    SPACE_AX  = next_id()
    SPACE_PL  = next_id()
    SPACE_BB  = next_id()
    SPACE_SR  = next_id()
    SPACE_SH  = next_id()
    SPACE     = next_id()
    SPACE_QA  = next_id()
    SPACE_QS  = next_id()
    REL_QS    = next_id()

    g = ifc_guid
    W = f"{width:.6f}"
    D = f"{depth:.6f}"
    code_name = kp["code"] + " " + kp["name"]

    lines += [
        f"#{ORIGIN}=IFCCARTESIANPOINT((0.,0.,0.));",
        f"#{AX3D_0}=IFCAXIS2PLACEMENT3D(#{ORIGIN},$,$);",
        f"#{GEOMCTX}=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-5,#{AX3D_0},$);",
        f"#{U_LEN}=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);",
        f"#{U_AREA}=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);",
        f"#{U_VOL}=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);",
        f"#{UNITS}=IFCUNITASSIGNMENT((#{U_LEN},#{U_AREA},#{U_VOL}));",
        f"#{PERSON}=IFCPERSON($,'Woodfine',$,$,$,$,$,$);",
        f"#{ORG_WFP}=IFCORGANIZATION($,'Woodfine Capital Projects Inc.',$,$,$);",
        f"#{ORG_WBL}=IFCORGANIZATION($,'Woodfine BIM Library',$,$,$);",
        f"#{PAO}=IFCPERSONANDORGANIZATION(#{PERSON},#{ORG_WFP},$);",
        f"#{APP}=IFCAPPLICATION(#{ORG_WBL},'1.0','generate-key-plans','WBL');",
        f"#{OWNHIST}=IFCOWNERHISTORY(#{PAO},#{APP},$,.ADDED.,1780339592,$,$,1780339592);",
        f"#{PROJ}=IFCPROJECT('{g()}',#{OWNHIST},'{kp['name']}',$,$,"
        + f"'Woodfine BIM Object Library',$,(#{GEOMCTX}),#{UNITS});",
        f"#{SITE_PL}=IFCLOCALPLACEMENT($,#{AX3D_0});",
        f"#{SITE}=IFCSITE('{g()}',#{OWNHIST},'Site',$,$,#{SITE_PL},$,.ELEMENT.,$,$,$,$,.0.,$);",
        f"#{BLDG_PL}=IFCLOCALPLACEMENT(#{SITE_PL},#{AX3D_0});",
        f"#{BLDG}=IFCBUILDING('{g()}',#{OWNHIST},'Building',$,$,#{BLDG_PL},$,.ELEMENT.,$,$,$);",
        f"#{STOREY_PL}=IFCLOCALPLACEMENT(#{BLDG_PL},#{AX3D_0});",
        f"#{STOREY}=IFCBUILDINGSTOREY('{g()}',#{OWNHIST},'Ground Floor',$,$,"
        + f"#{STOREY_PL},$,.ELEMENT.,0.,$);",
        f"#{SPACE_AX}=IFCAXIS2PLACEMENT3D(#{ORIGIN},$,$);",
        f"#{SPACE_PL}=IFCLOCALPLACEMENT(#{STOREY_PL},#{SPACE_AX});",
        f"#{SPACE_BB}=IFCBOUNDINGBOX(#{ORIGIN},{W},{D},3.500000);",
        f"#{SPACE_SR}=IFCSHAPEREPRESENTATION(#{GEOMCTX},'Body','BoundingBox',(#{SPACE_BB}));",
        f"#{SPACE_SH}=IFCPRODUCTDEFINITIONSHAPE($,$,(#{SPACE_SR}));",
        f"#{SPACE}=IFCSPACE('{g()}',#{OWNHIST},'{code_name}',$,"
        + f"'{kp['code']}',$,#{SPACE_PL},#{SPACE_SH},.ELEMENT.,.INTERNAL.,$);",
        f"#{SPACE_QA}=IFCQUANTITYAREA('NetFloorArea',$,$,{area:.6f},$);",
        f"#{SPACE_QS}=IFCELEMENTQUANTITY('{g()}',#{OWNHIST},'Qto_SpaceBaseQuantities',$,$,"
        + f"(#{SPACE_QA}));",
        f"#{REL_QS}=IFCRELDEFINESBYPROPERTIES('{g()}',#{OWNHIST},$,$,"
        + f"(#{SPACE}),#{SPACE_QS});",
    ]

    # Pset_SpaceCommon
    P_AREA_VAL = next_id()
    P_EXT_VAL  = next_id()
    PSET_SPc   = next_id()
    REL_PSET   = next_id()
    lines += [
        f"#{P_AREA_VAL}=IFCPROPERTYSINGLEVALUE('NetFloorArea',$,"
        + f"IFCAREAMEASURE({area:.6f}),$);",
        f"#{P_EXT_VAL}=IFCPROPERTYSINGLEVALUE('IsExternal',$,IFCBOOLEAN(.F.),$);",
        f"#{PSET_SPc}=IFCPROPERTYSET('{g()}',#{OWNHIST},'Pset_SpaceCommon',$,"
        + f"(#{P_AREA_VAL},#{P_EXT_VAL}));",
        f"#{REL_PSET}=IFCRELDEFINESBYPROPERTIES('{g()}',#{OWNHIST},$,$,"
        + f"(#{SPACE}),#{PSET_SPc});",
    ]

    # ── Furniture instances ──────────────────────────────────────────────────
    furn_ids = []
    for ftype, fx, fy in items:
        dim = FURN_DIMS[ftype]
        designation, style = FURN_PSET[ftype]
        f_pt  = next_id()
        f_ax  = next_id()
        f_pl  = next_id()
        f_bb  = next_id()
        f_sr  = next_id()
        f_sh  = next_id()
        f_obj = next_id()
        f_p1  = next_id()  # NominalLength
        f_p2  = next_id()  # NominalWidth
        f_p3  = next_id()  # NominalHeight
        f_p4  = next_id()  # FurnitureDesignation
        f_p5  = next_id()  # StyleDesignation
        f_ps  = next_id()  # Pset_FurnitureTypeCommon
        f_rp  = next_id()  # IfcRelDefinesByProperties
        furn_ids.append(f_obj)
        lines += [
            f"#{f_pt}=IFCCARTESIANPOINT(({fx:.4f},{fy:.4f},0.));",
            f"#{f_ax}=IFCAXIS2PLACEMENT3D(#{f_pt},$,$);",
            f"#{f_pl}=IFCLOCALPLACEMENT(#{STOREY_PL},#{f_ax});",
            f"#{f_bb}=IFCBOUNDINGBOX(#{ORIGIN},"
            + f"{dim['w']:.4f},{dim['d']:.4f},{dim['h']:.4f});",
            f"#{f_sr}=IFCSHAPEREPRESENTATION(#{GEOMCTX},'Body','BoundingBox',(#{f_bb}));",
            f"#{f_sh}=IFCPRODUCTDEFINITIONSHAPE($,$,(#{f_sr}));",
            f"#{f_obj}=IFCFURNITURE('{g()}',#{OWNHIST},'{designation}',$,"
            + f"'{ftype}',#{f_pl},#{f_sh},$);",
            f"#{f_p1}=IFCPROPERTYSINGLEVALUE('NominalLength',$,"
            + f"IFCLENGTHMEASURE({dim['w']:.4f}),$);",
            f"#{f_p2}=IFCPROPERTYSINGLEVALUE('NominalWidth',$,"
            + f"IFCLENGTHMEASURE({dim['d']:.4f}),$);",
            f"#{f_p3}=IFCPROPERTYSINGLEVALUE('NominalHeight',$,"
            + f"IFCLENGTHMEASURE({dim['h']:.4f}),$);",
            f"#{f_p4}=IFCPROPERTYSINGLEVALUE('FurnitureDesignation',$,"
            + f"IFCLABEL('{designation}'),$);",
            f"#{f_p5}=IFCPROPERTYSINGLEVALUE('StyleDesignation',$,"
            + f"IFCLABEL('{style}'),$);",
            f"#{f_ps}=IFCPROPERTYSET('{g()}',#{OWNHIST},'Pset_FurnitureTypeCommon',$,"
            + f"(#{f_p1},#{f_p2},#{f_p3},#{f_p4},#{f_p5}));",
            f"#{f_rp}=IFCRELDEFINESBYPROPERTIES('{g()}',#{OWNHIST},$,$,"
            + f"(#{f_obj}),#{f_ps});",
        ]

    # ── Aggregate + containment relationships ────────────────────────────────
    RA1 = next_id()
    RA2 = next_id()
    RA3 = next_id()
    RC1 = next_id()  # space contained in storey
    RC2 = next_id()  # furniture contained in storey (can be in space)
    RC3 = next_id()  # furniture in space
    furn_list = ",".join(f"#{f}" for f in furn_ids)
    lines += [
        f"#{RA1}=IFCRELAGGREGATES('{g()}',#{OWNHIST},$,$,#{PROJ},(#{SITE}));",
        f"#{RA2}=IFCRELAGGREGATES('{g()}',#{OWNHIST},$,$,#{SITE},(#{BLDG}));",
        f"#{RA3}=IFCRELAGGREGATES('{g()}',#{OWNHIST},$,$,#{BLDG},(#{STOREY}));",
        f"#{RC1}=IFCRELCONTAINEDINSPATIALSTRUCTURE('{g()}',#{OWNHIST},$,$,"
        + f"(#{SPACE}),#{STOREY});",
        f"#{RC3}=IFCRELCONTAINEDINSPATIALSTRUCTURE('{g()}',#{OWNHIST},$,$,"
        + f"({furn_list}),#{SPACE});",
    ]

    lines.append("ENDSEC;")
    lines.append("END-ISO-10303-21;")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo_root = Path(__file__).parent.parent
    out_dir = repo_root / "key-plans"
    out_dir.mkdir(exist_ok=True)

    for kp in KEY_PLANS:
        content = build_ifc(kp)
        out_path = out_dir / kp["filename"]
        out_path.write_text(content, encoding="utf-8")
        print(f"  wrote {out_path} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
