# woodfine-bim-library

Biblioteca de objetos BIM de Woodfine Management Corp. — paquete de objetos DTCG
para el Building Design System.

Almacén soberano de objetos BIM de nivel cliente para [bim.woodfinegroup.com](https://bim.woodfinegroup.com).
Sirve al motor de presentación `app-orchestration-bim` en tiempo de ejecución mediante la
variable de entorno `BIM_DESIGN_SYSTEM_DIR`.

---

## Categorías de objetos BIM

Nueve archivos de objetos DTCG que cubren las ocho categorías primitivas de IFC 4.3
más las especificaciones de rendimiento por zona climática:

| Archivo | Entidad IFC | Descripción |
|---|---|---|
| `tokens/bim/spatial.dtcg.json` | `IfcSpatialElement` | Objetos BIM de estructura espacial |
| `tokens/bim/elements.dtcg.json` | `IfcBuiltElement` | Objetos BIM de elementos construidos |
| `tokens/bim/systems.dtcg.json` | `IfcDistributionElement` | Objetos BIM de sistemas del edificio |
| `tokens/bim/materials.dtcg.json` | `IfcMaterial` | Objetos BIM de materiales |
| `tokens/bim/assemblies.dtcg.json` | `IfcElementAssembly` | Objetos BIM de ensamblajes |
| `tokens/bim/performance.dtcg.json` | `IfcPropertySet` | Objetos BIM de propiedades de rendimiento |
| `tokens/bim/identity-codes.dtcg.json` | `IfcClassificationReference` | Objetos BIM de identidad y clasificación |
| `tokens/bim/relationships.dtcg.json` | `IfcRel*` | Objetos BIM de relaciones |
| `tokens/bim/climate-zones.dtcg.json` | — | Especificaciones de rendimiento por zona climática |

Todos los archivos de tokens utilizan el formato
[W3C Design Token Community Group](https://design-tokens.github.io/community-group/format/)
(DTCG).

---

## Estándares

- **IFC 4.3** (ISO 16739-1:2024) — base de entidades
- **Uniclass 2015** — base de clasificación
- **IDS 1.0** — formato de restricciones para superposiciones regulatorias (en `regulation/`)
- **bSDD** (buildingSMART Data Dictionary) — autoridad de URIs

---

## Estructura del repositorio

```
tokens/bim/        ← Archivos de tokens DTCG (9 categorías)
regulation/        ← Superposiciones regulatorias (IDS 1.0 + fragmentos IFC); BC RS-1 en v0.0.3
climate/           ← Especificaciones de zona climática; bc-temperate-coastal en v0.0.3
components/        ← Recetas de componentes BIM
research/          ← Archivos de investigación legibles por IA
```

---

## Licencia

Licencia Apache 2.0 (Apache-2.0). Véase [LICENSE](LICENSE).
