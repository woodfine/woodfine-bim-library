#!/usr/bin/env python3
"""
Generate plan-view SVG symbols from DXF blocks in blocks/furniture/.

For each {slug}.dxf found in blocks/furniture/, produces a corresponding
{slug}.svg containing a clean architectural plan-view rendering.
Requires: ezdxf (pip install ezdxf)

Usage:
    python3 scripts/generate-furniture-plan-svg.py [--dxf-dir DIR] [--out-dir DIR]

The SVG output is used by app-orchestration-bim when serving the /furniture page.
If ezdxf is not installed, prints a download instruction and exits with code 1.
"""

import argparse
import os
import sys
from pathlib import Path


def check_ezdxf():
    try:
        import ezdxf
        return ezdxf
    except ImportError:
        print("ERROR: ezdxf is not installed.", file=sys.stderr)
        print("Install with: pip install ezdxf", file=sys.stderr)
        print("Or: pip3 install ezdxf", file=sys.stderr)
        sys.exit(1)


def dxf_to_svg(dxf_path: Path, svg_path: Path):
    """Convert a single DXF file to an architectural plan-view SVG."""
    ezdxf = check_ezdxf()
    from ezdxf import recover
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.svg import SVGBackend
    from ezdxf.addons.drawing.config import Configuration, ColorPolicy

    try:
        doc, auditor = recover.readfile(str(dxf_path))
    except Exception as e:
        print(f"  SKIP {dxf_path.name}: {e}", file=sys.stderr)
        return False

    msp = doc.modelspace()
    context = RenderContext(doc)
    config = Configuration.defaults()
    config = config.with_changes(
        color_policy=ColorPolicy.BLACK,
    )
    backend = SVGBackend()
    frontend = Frontend(context, backend, config=config)
    frontend.draw_layout(msp)

    settings = SVGBackend.Settings(size=(480, 480))
    svg_string = backend.get_xml_root_element(settings)

    import xml.etree.ElementTree as ET
    tree = ET.ElementTree(svg_string)
    tree.write(str(svg_path), encoding="unicode", xml_declaration=False)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    repo_root = Path(__file__).parent.parent
    parser.add_argument(
        "--dxf-dir",
        default=str(repo_root / "blocks" / "furniture"),
        help="Directory containing .dxf files (default: blocks/furniture/)",
    )
    parser.add_argument(
        "--out-dir",
        default=str(repo_root / "blocks" / "furniture"),
        help="Directory to write .svg files into (default: same as --dxf-dir)",
    )
    args = parser.parse_args()

    dxf_dir = Path(args.dxf_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dxf_files = sorted(dxf_dir.glob("*.dxf"))
    if not dxf_files:
        print(f"No .dxf files found in {dxf_dir}")
        print("Download manufacturer DXF files and place them as {slug}.dxf.")
        sys.exit(0)

    ok = 0
    for dxf_path in dxf_files:
        svg_path = out_dir / (dxf_path.stem + ".svg")
        print(f"  converting {dxf_path.name} → {svg_path.name}")
        if dxf_to_svg(dxf_path, svg_path):
            ok += 1

    print(f"\n{ok}/{len(dxf_files)} converted.")


if __name__ == "__main__":
    main()
