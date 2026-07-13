## ¿Qué es un Objeto BIM?

Un Objeto BIM es una especificación inteligente para una parte de un edificio. Geometría, datos de producto y las reglas que debe cumplir — reunidas en un solo archivo abierto que viaja con la parte a través de cada herramienta que la toca.

Cuando un arquitecto coloca un muro, el Objeto BIM del muro ya conoce su resistencia al fuego requerida, su rango de transmitancia térmica y qué disposición normativa lo rige en esa jurisdicción. La condicionante de cumplimiento está codificada en el material de partida — sin verificación posterior, sin un documento de especificación separado que pueda quedar desactualizado.

Todo Objeto responde tres preguntas:

1. **¿Qué es?** — su identidad formal: anclaje de entidad IFC 4.3, clasificación Uniclass 2015, conjuntos de propiedades.
2. **¿Qué debe cumplir?** — condicionantes normativos: disposiciones del código de construcción, resistencia al fuego, estándares energéticos, registrados contra el tipo de elemento.
3. **¿Dónde funciona?** — requisitos de desempeño por zona climática que cambian según la geografía (ASHRAE, NBC 2020).

### Detrás de escena — el modelo de datos

Cada Objeto BIM se almacena en formato JSON del W3C Design Token Community Group (DTCG) — un formato abierto, comparable línea por línea, sin contenedor propietario. Estándares base: IFC 4.3 (ISO 16739-1:2024), Uniclass 2015, IDS 1.0, bSDD.

## El modelo de contención

Un Objeto — un escritorio, una luminaria, una puerta — es una parte física. Un Key Plan, un Tile, una Placa de Piso, un Edificio es un volumen de espacio. La Biblioteca mantiene estas dos categorías estrictamente separadas, porque confundirlas es el error de categoría más común en el modelado de datos BIM: un muro no es una habitación, y una habitación no es un muro, aunque ambos sean cosas de las que un edificio está "hecho". El propio IFC 4.3 hace la misma distinción estructuralmente — un `IfcFurniture` y un `IfcSpace` son entidades fundamentalmente distintas, unidas por una relación "está ubicado en", no "es parte de".

**Los Objetos no se agregan hacia arriba.** Un Objeto es una parte independiente; nunca se suma en algo mayor de la forma en que un Key Plan se suma en un Tile. Cada Objeto colocado en un Key Plan queda registrado en la **lista de componentes** de ese Key Plan — un inventario de lo que contiene la habitación, no un nuevo peldaño por encima del Objeto mismo.

**Los Key Plan, Tiles y Placas de Piso se agregan — pero no por suma simple.** Un Tile no es Key Plan sumados entre sí, y una Placa de Piso no es Tiles sumados entre sí. Cada escala se anida en la que está por encima sin remanente, repitiendo el mismo arreglo autosimilar desde un solo Key Plan hasta el edificio completo.

**Las dos categorías se encuentran por contención, no por agregación.** Un Objeto está *colocado dentro* de un Key Plan — el escritorio está en la habitación, pero el escritorio no es "parte de" la habitación de la forma en que la habitación es parte del piso que está por encima de ella.

## Key Plan y Tile

Planeamos el espacio a partir del mobiliario hacia afuera, no de la superficie hacia adentro. Un **Key Plan** es la unidad mínima de espacio que vale la pena arrendar: un plano acotado a escala de habitación, definido por la disposición real del mobiliario, la circulación real y la luz natural real — no por una cuota de área. Los Key Plan se combinan en **Tiles**: bloques de Key Plan que cumplen doble función como la unidad que arrienda un inquilino y la zona que atienden los sistemas de servicios y climatización del edificio. Los Tiles se combinan en **Placas de Piso** — y una placa de piso ensamblada de esta forma llega con su luz, circulación y ventilación ya comprobadas en cada escala inferior. Esta componibilidad fraccional y autosimilar — un octavo, un cuarto, la mitad, tres cuartos, o una placa de piso completa — es nuestra propia extensión de la escalera de espacio. Key Plan es terminología real de dibujo técnico, aunque convencionalmente designa un diagrama de localización a pequeña escala y no una unidad arrendable a escala de habitación; Tile no tiene un equivalente estándar único en la práctica AEC, siendo los conceptos más cercanos una crujía estructural, un módulo de planeación, un lote de arrendamiento, o una zona de HVAC — ambos son nuestra propia operacionalización, en el mismo sentido que Habitat, Magazine y Corridor más abajo. Actualmente publicamos seis categorías de Key Plan arrendables — Oficina Privada, Médico, Negocios, Laboratorio, Académico, Cívico; las categorías de Amenidades y Área Común están en diseño activo y aún no se publican.

Cada Key Plan se resuelve en tres partes. **Hábitat:** donde trabaja la gente, contenido dentro de seis metros del perímetro del edificio para que cada puesto de trabajo reciba luz natural. **Magazine:** almacenamiento y profundidad flexible — la dimensión que solo se encuentra iterando planos reales, no por fórmula. **Corredor:** circulación, dimensionada según su propio Key Plan. Hábitat y Magazine se reflejan entre sí a través del Corredor. El ancho del edificio no se asume; se calcula hacia afuera a partir de estas tres partes. La lógica subyacente — una zona perimetral con luz natural, una zona interior flexible y una zona de circulación — es un principio bien establecido en la ciencia de la construcción y la planeación de espacios en general (la guía de HVAC por zona perimetral de ASHRAE, la Guide to Specification del British Council for Offices, los requisitos de zona con luz natural de LEED y WELL). Hábitat, Magazine y Corredor, y su acoplamiento con la Calculadora de Ancho de Edificación más abajo, son nuestra propia operacionalización de ese principio. También diseñamos cada Key Plan para que un inquilino pueda cumplir sus propios requisitos de certificación WELL directamente desde la geometría — luz, aire y circulación comprobados a escala de habitación, no asumidos y verificados después.

El argumento de eficiencia es específico: un plano construido a partir de mobiliario y circulación reales desperdicia menos área que un plano construido a partir de una fórmula de superficie. Desperdiciar menos área por inquilino permite construir menos área total mientras se aloja al mismo número de inquilinos — lo que eso significa para el argumento de sostenibilidad más amplio de la Biblioteca se desarrolla en Geometría de la Sostenibilidad, más abajo.

Los Key Plan están pensados para cubrir del 70 al 80% de los requisitos de certificación de un edificio directamente en su geometría — la circulación, la luz natural y la ventilación son visibles en la geometría misma, en lugar de reunirse después para una auditoría.

La vista de Objetos constituyentes de un Key Plan es su **lista de componentes** — cada Objeto colocado en ese Key Plan. Ver "El modelo de contención" más arriba para entender por qué esa relación es de contención, no de composición.

### La definición formal

Definimos "Key Plan y Tile" como un sistema de planeación espacial geométrico, autosimilar y aperiódico, basado en la disposición del mobiliario y el equipamiento y en la circulación, en lugar de una progresión modular de área por persona. En términos simples: el mismo patrón se repite en cada escala (autosimilar), no se repite sobre una cuadrícula fija (aperiódico), y su tamaño proviene del mobiliario y la circulación reales, no de una fórmula aplicada por persona o por pie cuadrado.

Los Key Plan se anidan en Tiles y Placas de Piso sin remanente, en ambas direcciones.

## Geometría de la Sostenibilidad

**Construir menos. Demostrarlo primero.**

La decisión de sostenibilidad más determinante en cualquier edificio se toma antes de que comience el diseño: cuánto edificio construir. Cada metro cuadrado que se levanta debe fabricarse, transportarse, ensamblarse, acondicionarse durante décadas y eventualmente desmontarse. Un edificio eficiente que es más grande de lo necesario sigue siendo una pérdida neta frente a uno más pequeño — ningún ahorro operativo compensa el área de piso que nunca debió existir. A esto le llamamos la reducción de la curva de producción — una forma sincera de sostenibilidad: menos construcción exigida al mundo por el mismo alojamiento entregado.

Lo que hace posible construir menos no es la restricción sino la comprobación. Los edificios se sobredimensionan por incertidumbre — una fórmula de área agrega margen a cada habitación, porque nadie sabe en la etapa de planeación si el mobiliario real, la circulación real, la luz natural real van a caber. El Key Plan elimina esa incertidumbre en la unidad mínima de espacio que vale la pena arrendar. Cada uno se dibuja a partir de la disposición real del mobiliario, la circulación real, la luz natural real, resolviéndose en las mismas tres partes descritas arriba — Hábitat, Magazine, Corredor — de modo que la luz, el aire y el movimiento no son compromisos que se verifican en auditoría; son visibles en el plano mismo.

Porque un Tile son Key Plan comprobados y una Placa de Piso son Tiles comprobados, esa confianza sobrevive la agregación. Un edificio compuesto de esta forma puede ser exactamente tan grande como lo requiere su alojamiento — sin margen por duda. Este es el primer pilar de la Geometría de la Sostenibilidad, y es la razón por la que va primero: la eficiencia mejora el edificio que se construye; la geometría decide cuánto edificio hay que mejorar.

Los otros dos pilares funcionan de la misma manera a otra escala: el paisaje (el estacionamiento reprogramado como un Jardín Forestal) y los materiales (seleccionados desde el inicio para reutilización adaptativa y minería urbana). Cada pilar es medible. Ninguno es aspiracional.

## Estándares

- **IFC 4.3** (ISO 16739-1:2024) — columna vertebral de entidades
- **Uniclass 2015** — piso de clasificación
- **IDS 1.0** — formato de condicionante normativo
- **bSDD** (buildingSMART Data Dictionary) — autoridad de URI
- **DTCG** — formato de token del W3C Design Token Community Group
