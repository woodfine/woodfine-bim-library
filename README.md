# woodfine-bim-library

Woodfine Management Corp. BIM Object library — DTCG object bundle
for the Building Design System.

Sovereign customer-tier BIM Object vault for [bim.woodfinegroup.com](https://bim.woodfinegroup.com).
Serves the `app-orchestration-bim` showcase engine at runtime via the
`BIM_DESIGN_SYSTEM_DIR` environment variable.

---

## BIM Object categories

Nine DTCG object files covering the eight IFC 4.3 primitive categories
plus climate zone performance specifications:

| File | IFC anchor | Description |
|---|---|---|
| `tokens/bim/spatial.dtcg.json` | `IfcSpatialElement` | Spatial structure BIM Objects |
| `tokens/bim/elements.dtcg.json` | `IfcBuiltElement` | Built element BIM Objects |
| `tokens/bim/systems.dtcg.json` | `IfcDistributionElement` | Building systems BIM Objects |
| `tokens/bim/materials.dtcg.json` | `IfcMaterial` | Material BIM Objects |
| `tokens/bim/assemblies.dtcg.json` | `IfcElementAssembly` | Assembly BIM Objects |
| `tokens/bim/performance.dtcg.json` | `IfcPropertySet` | Performance property BIM Objects |
| `tokens/bim/identity-codes.dtcg.json` | `IfcClassificationReference` | Identity and classification BIM Objects |
| `tokens/bim/relationships.dtcg.json` | `IfcRel*` | Relationship BIM Objects |
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

Apache License 2.0 (Apache-2.0). See [LICENSE](LICENSE).

<!-- BEGIN: factory-release-engineering license-section -->
<!-- ================================================================== -->
<!-- This section is generated from factory-release-engineering.         -->
<!-- Do not edit here. Propose changes upstream.                          -->
<!-- ================================================================== -->

## License

This repository is licensed under the **Apache-2.0**. See the
`LICENSE` file in the root of this repository for the full legal text,
which is authoritative.



Copyright © 2026 Woodfine Capital Projects Inc. — all rights not expressly
granted by the license are reserved.

<!-- ================================================================== -->
<!-- Esta sección se genera desde factory-release-engineering.           -->
<!-- No editar aquí. Proponga cambios río arriba.                         -->
<!-- ================================================================== -->

## Licencia

Este repositorio se distribuye bajo la **Apache-2.0**. Véase el
archivo `LICENSE` en la raíz del repositorio para consultar el texto
legal completo, el cual es la versión autoritativa.



Copyright © 2026 Woodfine Capital Projects Inc. — se reservan todos los
derechos no concedidos expresamente por la licencia.
<!-- END: factory-release-engineering license-section -->
