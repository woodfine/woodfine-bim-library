# Furniture Blocks

BIM Object blocks for the Private Office furniture program. Each file is a
self-contained BIM artifact for one of the 8 Steelcase / Coalesse pieces.

## IFC files (committed)

| File | Product | Manufacturer |
|---|---|---|
| `desk-steelcase-migration-se-58x29.ifc` | Migration SE Height-Adjustable Desk | Steelcase |
| `task-chair-steelcase-leap-v2.ifc` | Leap V2 Ergonomic Chair | Steelcase |
| `table-steelcase-groupwork-36.ifc` | Groupwork 36" Round Table | Steelcase |
| `credenza-steelcase-currency-credenza-72.ifc` | Currency Credenza 72" | Steelcase |
| `storage-steelcase-currency-bookcase-36.ifc` | Currency Bookcase 36" | Steelcase |
| `storage-steelcase-ts-mobile-pedestal.ifc` | TS Mobile Pedestal | Steelcase |
| `lounge-chair-coalesse-wing-ch445.ifc` | Wing Chair CH445 | Coalesse |
| `utility-generic-coat-rack.ifc` | Generic Coat Rack | — |

Served from `app-orchestration-bim` at `/furniture/download/{slug}.ifc`.

## DXF / RFA files (operator-placed, not committed)

Download manufacturer DXF and RFA files and place them here as
`{slug}.dxf` / `{slug}.rfa`. File naming mirrors the IFC slugs above.

Manufacturer download pages:
- Steelcase Migration SE: https://www.steelcase.com/products/height-adjustable-desks/migration-se/
- Steelcase Leap V2: https://www.steelcase.com/products/office-chairs/leap/
- Steelcase Groupwork 36": https://www.steelcase.com/products/conference-tables/groupwork/
- Steelcase Currency Credenza 72": https://www.steelcase.com/products/storage-solutions/currency/
- Steelcase Currency Bookcase 36": https://www.steelcase.com/products/storage-solutions/currency/
- Steelcase TS Mobile Pedestal: https://www.steelcase.com/products/storage-solutions/ts-series-storage/
- Coalesse Wing Chair CH445: https://www.coalesse.com/products/lounge-seating/wing/

## SVG plan symbols (generated)

After placing DXF files, run the pipeline to generate plan-view SVGs:

```bash
python3 scripts/generate-furniture-plan-svg.py
```

Or run the full nightly pipeline (also regenerates key plan IFC files):

```bash
bash scripts/run-furniture-pipeline.sh
```
