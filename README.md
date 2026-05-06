# woodfine-design-bim

Woodfine Management Corp. BIM design token library — DTCG token bundle
for the Building Design System.

Sovereign customer-tier BIM token vault for [bim.woodfinegroup.com](https://bim.woodfinegroup.com).
Serves the `app-orchestration-bim` showcase engine at runtime via the
`BIM_DESIGN_SYSTEM_DIR` environment variable.

---

## Token categories

Nine DTCG token files covering the eight IFC 4.3 primitive categories
plus climate zone performance specifications:

| File | IFC anchor | Description |
|---|---|---|
| `tokens/bim/spatial.dtcg.json` | `IfcSpatialElement` | Spatial structure tokens |
| `tokens/bim/elements.dtcg.json` | `IfcBuiltElement` | Built element tokens |
| `tokens/bim/systems.dtcg.json` | `IfcDistributionElement` | Building systems tokens |
| `tokens/bim/materials.dtcg.json` | `IfcMaterial` | Material tokens |
| `tokens/bim/assemblies.dtcg.json` | `IfcElementAssembly` | Assembly tokens |
| `tokens/bim/performance.dtcg.json` | `IfcPropertySet` | Performance property tokens |
| `tokens/bim/identity-codes.dtcg.json` | `IfcClassificationReference` | Identity and classification tokens |
| `tokens/bim/relationships.dtcg.json` | `IfcRel*` | Relationship tokens |
| `tokens/bim/climate-zones.dtcg.json` | — | Climate zone performance specifications |

All token files use the [W3C Design Token Community Group](https://design-tokens.github.io/community-group/format/)
(DTCG) format.

---

## Standards

- **IFC 4.3** (ISO 16739-1:2024) — entity backbone
- **Uniclass 2015** — classification floor
- **IDS 1.0** — regulatory overlay constraint format (in `regulation/`)
- **bSDD** (buildingSMART Data Dictionary) — URI authority

---

## Repository structure

```
tokens/bim/        ← DTCG token files (9 categories)
regulation/        ← Regulatory overlays (IDS 1.0 + IFC fragments); BC RS-1 at v0.0.3
climate/           ← Climate zone specifications; bc-temperate-coastal at v0.0.3
components/        ← BIM component recipes
research/          ← AI-readable research files
```

---

## License

European Union Public Licence v1.2 (EUPL-1.2). See [LICENSE](LICENSE).
