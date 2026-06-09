#!/usr/bin/env python3
"""
Generate IFC4 Key Plan compositions for woodfine-bim-library.

Each output file is a self-contained IFC4-SPF composition containing:
  - IfcSpace (room boundary with bounding-box geometry)
  - IfcFurniture instances placed at 2D plan coordinates
  - Pset_FurnitureTypeCommon property sets on each furniture item

Source: tokens/bim/key-plans.dtcg.json and tokens/bim/interior.dtcg.json
        V3 dimensions from Woodfine Management Corp. spatial taxonomy documents.

Output: key-plans/*.ifc (18 files: PO-1/2/3, M-1/2/3, B-1/2/3, L-1/2/3, A-1/2/3, C-1/2/3)

Usage: python3 scripts/generate-key-plans.py
"""

import uuid
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
# Key Plan definitions
# Zones (V3 Jan 2026 spatial taxonomy):
#   z1 = Habitat / façade depth (m)
#   z2 = Magazine / storage depth (m)
#   z3 = Corridor depth (m); 0.0 if no corridor zone
# Area: Professional Office grade (not Private Office)
# Width is computed: w = area / (z1 + z2 + z3)
# ---------------------------------------------------------------------------
KEY_PLANS = [
    # ── Private Office ────────────────────────────────────────────────────────
    {
        "code": "PO-1", "category": "private-office",
        "name": "Private Office — Small",
        "filename": "private-office-1.ifc",
        "area_m2": 30.19, "z1": 6.0, "z2": 3.8, "z3": 2.0, "size": "small",
    },
    {
        "code": "PO-2", "category": "private-office",
        "name": "Private Office — Medium",
        "filename": "private-office-2.ifc",
        "area_m2": 43.20, "z1": 6.0, "z2": 3.8, "z3": 2.0, "size": "medium",
    },
    {
        "code": "PO-3", "category": "private-office",
        "name": "Private Office — Large",
        "filename": "private-office-3.ifc",
        "area_m2": 63.64, "z1": 6.0, "z2": 3.8, "z3": 2.0, "size": "large",
    },
    # ── Medical ───────────────────────────────────────────────────────────────
    # Z1=7.2m (exam rooms/façade), Z2=4.9m (offices+reception), Z3=2.9m (corridor)
    {
        "code": "M-1", "category": "medical",
        "name": "Professional Office — Medical — Small",
        "filename": "medical-1.ifc",
        "area_m2": 223.0, "z1": 7.2, "z2": 4.9, "z3": 2.9, "size": "small",
    },
    {
        "code": "M-2", "category": "medical",
        "name": "Professional Office — Medical — Medium",
        "filename": "medical-2.ifc",
        "area_m2": 331.0, "z1": 7.2, "z2": 4.9, "z3": 2.9, "size": "medium",
    },
    {
        "code": "M-3", "category": "medical",
        "name": "Professional Office — Medical — Large",
        "filename": "medical-3.ifc",
        "area_m2": 486.0, "z1": 7.2, "z2": 4.9, "z3": 2.9, "size": "large",
    },
    # ── Business ──────────────────────────────────────────────────────────────
    # Z1=6.0m (exec+manager offices/façade), Z2=7.3m (associates+conference), Z3=2.7m (reception/corridor)
    {
        "code": "B-1", "category": "business",
        "name": "Professional Office — Business — Small",
        "filename": "business-1.ifc",
        "area_m2": 311.22, "z1": 6.0, "z2": 7.3, "z3": 2.7, "size": "small",
    },
    {
        "code": "B-2", "category": "business",
        "name": "Professional Office — Business — Medium",
        "filename": "business-2.ifc",
        "area_m2": 399.66, "z1": 6.0, "z2": 7.3, "z3": 2.7, "size": "medium",
    },
    {
        "code": "B-3", "category": "business",
        "name": "Professional Office — Business — Large",
        "filename": "business-3.ifc",
        "area_m2": 669.0, "z1": 6.0, "z2": 7.3, "z3": 2.7, "size": "large",
    },
    # ── Laboratory ────────────────────────────────────────────────────────────
    # Z1=6.8m (lab benches/façade), Z2=4.8m (offices+reception), Z3=3.0m (clean room/corridor)
    {
        "code": "L-1", "category": "laboratory",
        "name": "Professional Office — Laboratory — Small",
        "filename": "laboratory-1.ifc",
        "area_m2": 195.0, "z1": 6.8, "z2": 4.8, "z3": 3.0, "size": "small",
    },
    {
        "code": "L-2", "category": "laboratory",
        "name": "Professional Office — Laboratory — Medium",
        "filename": "laboratory-2.ifc",
        "area_m2": 315.96, "z1": 6.8, "z2": 4.8, "z3": 3.0, "size": "medium",
    },
    {
        "code": "L-3", "category": "laboratory",
        "name": "Professional Office — Laboratory — Large",
        "filename": "laboratory-3.ifc",
        "area_m2": 400.69, "z1": 6.8, "z2": 4.8, "z3": 3.0, "size": "large",
    },
    # ── Academic ──────────────────────────────────────────────────────────────
    # Z1=4.7m (offices+seminar/façade), Z2=3.0m (reception+staff), Z3=0m (no separate corridor)
    {
        "code": "A-1", "category": "academic",
        "name": "Professional Office — Academic — Small",
        "filename": "academic-1.ifc",
        "area_m2": 105.0, "z1": 4.7, "z2": 3.0, "z3": 0.0, "size": "small",
    },
    {
        "code": "A-2", "category": "academic",
        "name": "Professional Office — Academic — Medium",
        "filename": "academic-2.ifc",
        "area_m2": 240.0, "z1": 4.7, "z2": 3.0, "z3": 0.0, "size": "medium",
    },
    {
        "code": "A-3", "category": "academic",
        "name": "Professional Office — Academic — Large",
        "filename": "academic-3.ifc",
        "area_m2": 378.0, "z1": 4.7, "z2": 3.0, "z3": 0.0, "size": "large",
    },
    # ── Civic ────────────────────────────────────────────────────────────────
    # Z1=6.0m (offices+conference/façade), Z2=7.2m (open+reception), Z3=3.6m (corridor+restroom)
    {
        "code": "C-1", "category": "civic",
        "name": "Professional Office — Civic — Small",
        "filename": "civic-1.ifc",
        "area_m2": 270.0, "z1": 6.0, "z2": 7.2, "z3": 3.6, "size": "small",
    },
    {
        "code": "C-2", "category": "civic",
        "name": "Professional Office — Civic — Medium",
        "filename": "civic-2.ifc",
        "area_m2": 577.0, "z1": 6.0, "z2": 7.2, "z3": 3.6, "size": "medium",
    },
    {
        "code": "C-3", "category": "civic",
        "name": "Professional Office — Civic — Large",
        "filename": "civic-3.ifc",
        "area_m2": 822.0, "z1": 6.0, "z2": 7.2, "z3": 3.6, "size": "large",
    },
]

# ---------------------------------------------------------------------------
# Furniture dimensions in metres
# ---------------------------------------------------------------------------
FURN_DIMS = {
    # Private Office furniture (Steelcase/Coalesse)
    "desk":          {"w": 1.473, "d": 0.737, "h": 0.574},   # Migration SE 58x29
    "chair":         {"w": 0.686, "d": 0.629, "h": 0.978},   # Leap V2
    "table":         {"w": 0.914, "d": 0.914, "h": 0.724},   # Groupwork 36" round
    "credenza":      {"w": 1.830, "d": 0.457, "h": 0.737},   # Currency Credenza 72"
    "bookcase":      {"w": 0.914, "d": 0.381, "h": 1.846},   # Currency Bookcase 36"
    "pedestal":      {"w": 0.387, "d": 0.559, "h": 0.533},   # TS Mobile Pedestal
    "lounge":        {"w": 0.899, "d": 0.896, "h": 1.031},   # Wing Chair CH445
    "coat_rack":     {"w": 0.400, "d": 0.300, "h": 1.800},   # Generic Coat Rack
    # Medical furniture
    "exam_table":    {"w": 1.830, "d": 0.760, "h": 0.800},   # Midmark Ritter 204
    "exam_stool":    {"w": 0.400, "d": 0.400, "h": 0.530},   # Exam Stool
    "waiting_chair": {"w": 0.560, "d": 0.560, "h": 0.830},   # Side Chair (waiting)
    "lab_bench":     {"w": 1.830, "d": 0.760, "h": 0.900},   # Lab Bench 72"
    "lab_stool":     {"w": 0.400, "d": 0.400, "h": 0.750},   # Lab Stool
    # Business furniture
    "conf_table":    {"w": 3.660, "d": 1.070, "h": 0.740},   # Conference Table 12ft
    # Academic furniture
    "seminar_table": {"w": 1.520, "d": 0.610, "h": 0.740},   # Seminar Table 60"
    "podium":        {"w": 0.610, "d": 0.460, "h": 1.070},   # Lecture Podium
    # Civic furniture
    "judge_bench":   {"w": 2.440, "d": 0.910, "h": 0.910},   # Judge's Bench
    "conf_bench":    {"w": 2.440, "d": 0.760, "h": 0.740},   # Conference Bench (gallery)
}

# Pset_FurnitureTypeCommon designations
FURN_PSET = {
    "desk":          ("Steelcase Migration SE Height-Adjustable Desk", "58\" x 29\" Rectangle"),
    "chair":         ("Steelcase Leap V2 Ergonomic Chair",            "Task Chair"),
    "table":         ("Steelcase Groupwork 36-Inch Round Table",      "Working Height Round Table"),
    "credenza":      ("Steelcase Currency Credenza 72\"",             "Credenza Storage"),
    "bookcase":      ("Steelcase Currency Bookcase 36\"",             "Upright Bookcase"),
    "pedestal":      ("Steelcase TS Mobile Pedestal",                 "Mobile Storage Pedestal"),
    "lounge":        ("Coalesse Wing Chair CH445",                    "Lounge Seating"),
    "coat_rack":     ("Generic Coat Rack",                            "Freestanding Hook Panel"),
    "exam_table":    ("Midmark Ritter 204 Power Exam Table",          "Medical Examination Table"),
    "exam_stool":    ("Medical Exam Stool",                           "Adjustable Exam Stool"),
    "waiting_chair": ("Side Chair — Waiting Room",                    "Stacking Guest Chair"),
    "lab_bench":     ("Laboratory Bench 72-Inch",                     "Fixed Lab Bench"),
    "lab_stool":     ("Laboratory Stool",                             "Adjustable Lab Stool"),
    "conf_table":    ("Conference Table 12-Foot Rectangular",         "Boardroom Table"),
    "seminar_table": ("Seminar Table 60-Inch",                        "Folding Seminar Table"),
    "podium":        ("Lecture Podium",                               "Presentation Podium"),
    "judge_bench":   ("Judge's Bench",                                "Elevated Judicial Bench"),
    "conf_bench":    ("Conference Gallery Bench",                     "Fixed Gallery Bench"),
}


# ---------------------------------------------------------------------------
# Furniture layout functions — one per category
# ---------------------------------------------------------------------------

def _compute_width(kp):
    depth = kp["z1"] + kp["z2"] + kp["z3"]
    return kp["area_m2"] / depth


def furniture_layout(kp):
    """Private Office layout (PO-1/2/3)."""
    w = _compute_width(kp)
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []

    # Zone 1 — desk + chair + table
    desk_x = 0.10
    desk_y = z1_start + 0.10
    items.append(("desk", desk_x, desk_y))
    items.append(("chair",
                  desk_x + (FURN_DIMS["desk"]["w"] - FURN_DIMS["chair"]["w"]) / 2,
                  desk_y + FURN_DIMS["desk"]["d"] + 0.20))
    items.append(("pedestal", desk_x + FURN_DIMS["desk"]["w"] + 0.10, desk_y))

    if kp["size"] == "small":
        tbl_x = max(desk_x + FURN_DIMS["desk"]["w"] + 0.50,
                    w / 2 - FURN_DIMS["table"]["w"] / 2)
        tbl_y = z1_start + kp["z1"] * 0.45
    elif kp["size"] == "medium":
        tbl_x = w / 2 - FURN_DIMS["table"]["w"] / 2
        tbl_y = z1_start + kp["z1"] * 0.40
    else:
        tbl_x = w * 0.35
        tbl_y = z1_start + kp["z1"] * 0.38
    items.append(("table", tbl_x, tbl_y))

    if kp["size"] == "large":
        items.append(("lounge", w - FURN_DIMS["lounge"]["w"] - 0.10,
                      z1_start + kp["z1"] * 0.60))

    # Zone 2 — credenza + bookcase
    items.append(("credenza", 0.10, z2_start + 0.10))
    bookcase_x = min(0.10 + FURN_DIMS["credenza"]["w"] + 0.20,
                     w - FURN_DIMS["bookcase"]["w"] - 0.10)
    items.append(("bookcase", bookcase_x, z2_start + 0.10))

    # Zone 3 — coat rack
    items.append(("coat_rack", w - FURN_DIMS["coat_rack"]["w"] - 0.10, 0.10))

    return items, w


def furniture_layout_medical(kp):
    """Medical layout: exam tables (Z1/façade), offices+reception (Z2), corridor (Z3)."""
    w = _compute_width(kp)
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []
    exam_count = {"small": 3, "medium": 5, "large": 7}[kp["size"]]
    et_w = FURN_DIMS["exam_table"]["w"]
    et_d = FURN_DIMS["exam_table"]["d"]
    es_w = FURN_DIMS["exam_stool"]["w"]

    # Zone 1 — exam tables in a row with stools
    spacing = (w - 0.20) / exam_count
    for i in range(exam_count):
        ex = 0.10 + i * spacing
        ey = z1_start + 0.20
        items.append(("exam_table", ex, ey))
        items.append(("exam_stool", ex + (et_w - es_w) / 2, ey + et_d + 0.15))

    # Zone 2 — doctor's desk left, reception desk right, credenza
    items.append(("desk", 0.10, z2_start + 0.15))
    items.append(("chair", 0.10 + (FURN_DIMS["desk"]["w"] - FURN_DIMS["chair"]["w"]) / 2,
                  z2_start + 0.15 + FURN_DIMS["desk"]["d"] + 0.20))
    if kp["size"] in ("medium", "large"):
        items.append(("desk", w * 0.55, z2_start + 0.15))
        items.append(("chair",
                      w * 0.55 + (FURN_DIMS["desk"]["w"] - FURN_DIMS["chair"]["w"]) / 2,
                      z2_start + 0.15 + FURN_DIMS["desk"]["d"] + 0.20))
    items.append(("credenza", w - FURN_DIMS["credenza"]["w"] - 0.10, z2_start + 0.15))

    # Zone 3 — waiting chairs near entry
    wc_w = FURN_DIMS["waiting_chair"]["w"]
    seat_count = {"small": 6, "medium": 10, "large": 10}[kp["size"]]
    for i in range(min(seat_count, int(w / (wc_w + 0.15)))):
        items.append(("waiting_chair", 0.10 + i * (wc_w + 0.15), z3 * 0.25))

    return items, w


def furniture_layout_business(kp):
    """Business layout: exec+manager offices (Z1/façade), associates+conference (Z2), reception (Z3)."""
    w = _compute_width(kp)
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []
    desk_w = FURN_DIMS["desk"]["w"]
    desk_d = FURN_DIMS["desk"]["d"]
    chair_w = FURN_DIMS["chair"]["w"]

    exec_count  = {"small": 1, "medium": 1, "large": 2}[kp["size"]]
    mgr_count   = {"small": 1, "medium": 2, "large": 3}[kp["size"]]
    assoc_count = {"small": 3, "medium": 5, "large": 7}[kp["size"]]

    # Zone 1 — executive desks left, manager desks right
    office_w = w / (exec_count + mgr_count + 0.5)
    pos = 0.10
    for _ in range(exec_count):
        items.append(("desk", pos, z1_start + 0.15))
        items.append(("chair", pos + (desk_w - chair_w) / 2,
                      z1_start + 0.15 + desk_d + 0.20))
        items.append(("table", pos + desk_w + 0.30, z1_start + kp["z1"] * 0.40))
        items.append(("bookcase", pos + desk_w + 0.30, z1_start + 0.10))
        pos += office_w
    for _ in range(mgr_count):
        items.append(("desk", pos, z1_start + 0.15))
        items.append(("chair", pos + (desk_w - chair_w) / 2,
                      z1_start + 0.15 + desk_d + 0.20))
        items.append(("bookcase", pos, z1_start + 0.10))
        pos += office_w

    # Zone 2 — associate workstations + conference table
    assoc_spacing = min(desk_w + 0.30, (w * 0.55) / max(assoc_count, 1))
    for i in range(assoc_count):
        ax = 0.10 + i * assoc_spacing
        items.append(("desk", ax, z2_start + 0.15))
        items.append(("chair", ax + (desk_w - chair_w) / 2,
                      z2_start + 0.15 + desk_d + 0.20))

    ct_w = FURN_DIMS["conf_table"]["w"]
    ct_x = w - ct_w - 0.20
    ct_y = z2_start + (kp["z2"] - FURN_DIMS["conf_table"]["d"]) / 2
    items.append(("conf_table", ct_x, ct_y))
    conf_chair_count = {"small": 4, "medium": 6, "large": 8}[kp["size"]]
    cc_spacing = ct_w / (conf_chair_count / 2 + 1)
    for i in range(conf_chair_count // 2):
        items.append(("chair", ct_x + cc_spacing * (i + 1),
                      ct_y - FURN_DIMS["chair"]["d"] - 0.10))
        items.append(("chair", ct_x + cc_spacing * (i + 1),
                      ct_y + FURN_DIMS["conf_table"]["d"] + 0.10))

    # Zone 3 — reception desk + waiting chairs
    items.append(("desk", 0.10, 0.15))
    items.append(("chair", 0.10 + (desk_w - chair_w) / 2,
                  0.15 + desk_d + 0.20))
    items.append(("credenza", 0.10 + desk_w + 0.20, 0.15))
    wc_w = FURN_DIMS["waiting_chair"]["w"]
    seat_count = {"small": 4, "medium": 6, "large": 6}[kp["size"]]
    wx_start = w - (seat_count * (wc_w + 0.15)) - 0.10
    for i in range(seat_count):
        items.append(("waiting_chair", wx_start + i * (wc_w + 0.15), 0.15))

    return items, w


def furniture_layout_laboratory(kp):
    """Laboratory layout: lab benches (Z1/façade), offices+reception (Z2), clean room (Z3)."""
    w = _compute_width(kp)
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []
    bench_count = {"small": 3, "medium": 5, "large": 7}[kp["size"]]
    lb_w = FURN_DIMS["lab_bench"]["w"]
    lb_d = FURN_DIMS["lab_bench"]["d"]
    ls_w = FURN_DIMS["lab_stool"]["w"]

    # Zone 1 — lab benches in row with stools
    spacing = (w - 0.20) / bench_count
    for i in range(bench_count):
        bx = 0.10 + i * spacing
        by = z1_start + 0.15
        items.append(("lab_bench", bx, by))
        items.append(("lab_stool", bx + (lb_w - ls_w) / 2, by + lb_d + 0.20))

    # Zone 2 — doctor's office(s) left + reception right
    desk_w = FURN_DIMS["desk"]["w"]
    desk_d = FURN_DIMS["desk"]["d"]
    chair_w = FURN_DIMS["chair"]["w"]
    doc_count = {"small": 1, "medium": 2, "large": 2}[kp["size"]]
    for i in range(doc_count):
        dx = 0.10 + i * (desk_w + 1.20)
        items.append(("desk", dx, z2_start + 0.15))
        items.append(("chair", dx + (desk_w - chair_w) / 2,
                      z2_start + 0.15 + desk_d + 0.20))
    items.append(("credenza", w - FURN_DIMS["credenza"]["w"] - 0.10, z2_start + 0.15))

    # Zone 3 — clean room bench + hazmat storage stub
    items.append(("lab_bench", 0.10, 0.15))
    items.append(("lab_stool", 0.10 + (lb_w - ls_w) / 2, 0.15 + lb_d + 0.20))
    if kp["size"] == "large":
        items.append(("lab_bench", 0.10 + lb_w + 0.40, 0.15))

    return items, w


def furniture_layout_academic(kp):
    """Academic layout: offices+seminar (Z1/façade), reception+staff (Z2). No Z3."""
    w = _compute_width(kp)
    # Academic has no Z3; z3=0
    z2_start = 0.0
    z1_start = kp["z2"]

    items = []
    desk_w = FURN_DIMS["desk"]["w"]
    desk_d = FURN_DIMS["desk"]["d"]
    chair_w = FURN_DIMS["chair"]["w"]
    st_w = FURN_DIMS["seminar_table"]["w"]
    st_d = FURN_DIMS["seminar_table"]["d"]

    office_count  = {"small": 2, "medium": 4, "large": 5}[kp["size"]]
    seminar_count = {"small": 1, "medium": 2, "large": 2}[kp["size"]]

    # Zone 1 — offices left, seminar rooms right
    office_bay = w / (office_count + seminar_count * 1.5)
    pos = 0.10
    for _ in range(office_count):
        items.append(("desk", pos, z1_start + 0.15))
        items.append(("chair", pos + (desk_w - chair_w) / 2,
                      z1_start + 0.15 + desk_d + 0.20))
        items.append(("bookcase", pos, z1_start + 0.10))
        pos += office_bay

    for _ in range(seminar_count):
        # Seminar tables in 2 rows
        for row in range(2):
            for col in range({"small": 2, "medium": 4, "large": 4}[kp["size"]] // seminar_count):
                sx = pos + col * (st_w + 0.10)
                sy = z1_start + 0.15 + row * (st_d + 0.60)
                items.append(("seminar_table", sx, sy))
                items.append(("chair", sx + (st_w - chair_w) / 2, sy + st_d + 0.15))
        items.append(("podium", pos, z1_start + kp["z1"] - FURN_DIMS["podium"]["d"] - 0.20))
        pos += office_bay * 1.5

    # Large: auditorium section at far right
    if kp["size"] == "large" and w > 40.0:
        aud_x = w * 0.75
        items.append(("podium", aud_x, z1_start + 0.20))
        # Theater-style rows of chairs
        for row in range(4):
            for col in range(8):
                items.append(("waiting_chair",
                               aud_x + col * (FURN_DIMS["waiting_chair"]["w"] + 0.10),
                               z1_start + 0.80 + row * (FURN_DIMS["waiting_chair"]["d"] + 0.40)))

    # Zone 2 — reception desk + staff area
    items.append(("desk", 0.10, z2_start + 0.15))
    items.append(("chair", 0.10 + (desk_w - chair_w) / 2,
                  z2_start + 0.15 + desk_d + 0.20))
    items.append(("credenza", 0.10 + desk_w + 0.20, z2_start + 0.15))
    wc_w = FURN_DIMS["waiting_chair"]["w"]
    seat_count = {"small": 4, "medium": 8, "large": 10}[kp["size"]]
    for i in range(min(seat_count, int(w * 0.4 / (wc_w + 0.15)))):
        items.append(("waiting_chair",
                      w * 0.50 + i * (wc_w + 0.15),
                      z2_start + 0.20))

    return items, w


def furniture_layout_civic(kp):
    """Civic layout: offices+conference (Z1/façade), open+reception (Z2), corridor (Z3)."""
    w = _compute_width(kp)
    z3 = kp["z3"]
    z2_start = z3
    z1_start = z3 + kp["z2"]

    items = []
    desk_w = FURN_DIMS["desk"]["w"]
    desk_d = FURN_DIMS["desk"]["d"]
    chair_w = FURN_DIMS["chair"]["w"]
    ct_w = FURN_DIMS["conf_table"]["w"]

    office_count = {"small": 2, "medium": 4, "large": 5}[kp["size"]]
    conf_count   = {"small": 1, "medium": 2, "large": 2}[kp["size"]]

    # Zone 1 — offices left, conference rooms right
    bay_count = office_count + conf_count + (1 if kp["size"] == "large" else 0)
    bay_w = w / bay_count
    pos = 0.10

    for _ in range(office_count):
        items.append(("desk", pos, z1_start + 0.15))
        items.append(("chair", pos + (desk_w - chair_w) / 2,
                      z1_start + 0.15 + desk_d + 0.20))
        items.append(("bookcase", pos, z1_start + 0.10))
        pos += bay_w

    for _ in range(conf_count):
        items.append(("conf_table", pos + 0.20, z1_start + 0.30))
        cc_count = {"small": 8, "medium": 16, "large": 16}[kp["size"]] // conf_count
        cc_spacing = ct_w / (cc_count / 2 + 1)
        for i in range(cc_count // 2):
            items.append(("chair", pos + 0.20 + cc_spacing * (i + 1),
                          z1_start + 0.30 - FURN_DIMS["chair"]["d"] - 0.10))
            items.append(("chair", pos + 0.20 + cc_spacing * (i + 1),
                          z1_start + 0.30 + FURN_DIMS["conf_table"]["d"] + 0.10))
        pos += bay_w

    # Large: court room section at far right
    if kp["size"] == "large":
        jb_x = w - FURN_DIMS["judge_bench"]["w"] - 0.20
        jb_y = z1_start + kp["z1"] - FURN_DIMS["judge_bench"]["d"] - 0.20
        items.append(("judge_bench", jb_x, jb_y))
        # gallery bench rows
        for row in range(3):
            items.append(("conf_bench", pos + 0.20,
                           z1_start + 0.30 + row * (FURN_DIMS["conf_bench"]["d"] + 0.50)))

    # Zone 2 — reception + open seating
    items.append(("desk", 0.10, z2_start + 0.15))
    items.append(("chair", 0.10 + (desk_w - chair_w) / 2,
                  z2_start + 0.15 + desk_d + 0.20))
    items.append(("credenza", 0.10 + desk_w + 0.20, z2_start + 0.15))
    wc_w = FURN_DIMS["waiting_chair"]["w"]
    seat_count = {"small": 2, "medium": 6, "large": 8}[kp["size"]]
    for i in range(seat_count):
        items.append(("waiting_chair",
                      w * 0.55 + i * (wc_w + 0.15),
                      z2_start + 0.25))

    # Zone 3 — corridor (coat rack stub)
    items.append(("coat_rack", w - FURN_DIMS["coat_rack"]["w"] - 0.10, 0.10))

    return items, w


# ---------------------------------------------------------------------------
# Layout dispatcher
# ---------------------------------------------------------------------------
_LAYOUT_FN = {
    "private-office": furniture_layout,
    "medical":        furniture_layout_medical,
    "business":       furniture_layout_business,
    "laboratory":     furniture_layout_laboratory,
    "academic":       furniture_layout_academic,
    "civic":          furniture_layout_civic,
}


# ---------------------------------------------------------------------------
# IFC-SPF builder
# ---------------------------------------------------------------------------

def build_ifc(kp):
    """Return complete IFC4-SPF file content as a string."""
    depth = kp["z1"] + kp["z2"] + kp["z3"]
    layout_fn = _LAYOUT_FN[kp["category"]]
    items, width = layout_fn(kp)
    area = kp["area_m2"]

    id_ = 10
    def next_id():
        nonlocal id_
        v = id_; id_ += 10; return v

    lines = []

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
        f"FILE_NAME('{kp_file}','2026-06-09T00:00:00',"
        "(''),'','woodfine-bim-library generate-key-plans','','');"
    )
    lines.append("FILE_SCHEMA(('IFC4'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")

    ORIGIN    = next_id()
    AX3D_0    = next_id()
    GEOMCTX   = next_id()
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
    SITE_PL   = next_id()
    SITE      = next_id()
    BLDG_PL   = next_id()
    BLDG      = next_id()
    STOREY_PL = next_id()
    STOREY    = next_id()
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
        f_p1  = next_id()
        f_p2  = next_id()
        f_p3  = next_id()
        f_p4  = next_id()
        f_p5  = next_id()
        f_ps  = next_id()
        f_rp  = next_id()
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

    RA1 = next_id()
    RA2 = next_id()
    RA3 = next_id()
    RC1 = next_id()
    RC3 = next_id()
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
        print(f"  wrote {out_path.name} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
