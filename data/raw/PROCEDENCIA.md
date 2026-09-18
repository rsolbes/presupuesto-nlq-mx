# Procedencia de las fuentes crudas

Registro de cada archivo de `data/raw/`: de dónde se obtuvo, cuándo, con qué huella digital y qué papel cumple en el proyecto. Los archivos no se versionan por su tamaño; este registro sí.

Los portales oficiales republican y corrigen sus archivos sin aviso. La huella SHA-256 permite comprobar que un archivo es exactamente el que se usó: si alguien descarga hoy el mismo conjunto y su huella difiere, la fuente cambió y los resultados de este trabajo no son directamente comparables.

**Fecha de obtención:** 17 de septiembre de 2026, descarga manual. El Portal de Transparencia Presupuestaria bloquea el acceso automatizado. La hora de cada archivo corresponde a su marca de tiempo en disco.

## Cómo verificar una huella

En PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 data\raw\cuenta_publica_2024_gf_ecd_epe.xlsx
```

En Bash:

```bash
sha256sum data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx
```

## 1. Fuentes cargadas a la base

Estado Analítico del Ejercicio del Presupuesto de Egresos, Cuenta Pública federal. Portal de Transparencia Presupuestaria (SHCP), sección Datos abiertos.

Para 2020 a 2024 se carga el xlsx porque los CSV publicados pierden renglones en todos esos ejercicios, y el de 2024 además reporta 9,699 millones de pesos de más en el ramo 51, cifra que no coincide con el informe oficial de Cuenta Pública (ver sección 4). Para 2025 ambos formatos son idénticos al peso y se usa el CSV. Detalle en `experiments/salidas/cruce_xlsx_csv.md`.

| Archivo | Hora | Bytes | SHA-256 | URL de origen |
|---|---|---:|---|---|
| `cuenta_publica_2020_gf_ecd_epe.xlsx` | 17:19 | 30,817,534 | `d1b519f0ad80c3ea1c356118fbbaa30c494510ad9a004f6913e1dbf13f008555` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2020_gf_ecd_epe.xlsx |
| `cuenta_publica_2021_gf_ecd_epe.xlsx` | 17:19 | 30,868,637 | `b04dce2c37f208edc77fc3fad890eb66bf4391cbf37dd6e077a67b04a259de57` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2021_gf_ecd_epe.xlsx |
| `cuenta_publica_2022_gf_ecd_epe.xlsx` | 17:03 | 68,310,826 | `154570ea2f432829dff5a1f74f4c92c3272edee6fa97d6663cf89293cb2cd494` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2022_gf_ecd_epe.xlsx |
| `cuenta_publica_2023_gf_ecd_epe.xlsx` | 17:19 | 27,700,951 | `5cbe7a788ae387d8379f1ac9e59c9b4c86e87d40bce8ce49e371a020902b5b50` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2023_gf_ecd_epe.xlsx |
| `cuenta_publica_2024_gf_ecd_epe.xlsx` | 17:19 | 28,667,352 | `3f508529ca92ca29cd918abe282f8e2b4282f63e65d61b0242945765c251aa55` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2024_gf_ecd_epe.xlsx |
| `cuenta_publica_2025_gf_ecd_epe.csv` | 16:55 | 105,584,237 | `973aab21969233bdfad3c4f87ccd467ab92421ea5c2cd249644c0bf2f7f1d0c0` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2025_gf_ecd_epe.csv |

## 2. Conservadas como evidencia, no cargadas

Los CSV publicados de 2020 a 2024 no se cargan, pero se conservan porque son la evidencia de sus defectos: renglones malformados por errores de escapado en todos ellos; celdas de importe vacías en 2021 que el xlsx sí trae; 828,067 renglones de relleno y 180 columnas sin nombre en 2022; una descripción corrompida en 2024 (`Desarrollo SoSocial`) y la discrepancia del ISSSTE. Borrarlos eliminaría la posibilidad de verificar esos hallazgos.

El xlsx de 2025 se conserva como contraparte del CSV cargado: su coincidencia exacta es lo que justifica usar el CSV en ese ejercicio.

| Archivo | Hora | Bytes | SHA-256 | Defecto documentado | URL de origen |
|---|---|---:|---|---|---|
| `cuenta_publica_2020_gf_ecd_epe.csv` | 16:43 | 106,551,620 | `4366e7e1be1f70bb14811b38a45737416b62d20d0063deda12c213dfe340929e` | pierde 10 renglones | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2020_gf_ecd_epe.csv |
| `cuenta_publica_2021_gf_ecd_epe.csv` | 16:40 | 112,193,350 | `617a6e4aac9b1297790c0138a15891027adb5c7cbb81499e4801eef9d3fdeec4` | pierde 2 renglones; importes en blanco | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2021_gf_ecd_epe.csv |
| `cuenta_publica_2022_gf_ecd_epe.csv` | 16:52 | 326,032,294 | `59e4e5158f199968a8f654c0ee6540d2a4a218cb5fd9da25414fdfbc54ef47f0` | pierde 3 renglones; 828,067 de relleno | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2022_gf_ecd_epe.csv |
| `cuenta_publica_2023_gf_ecd_epe.csv` | 16:40 | 100,932,349 | `1c58da6166e1a97cbc2f213c2a3c41e5577d337a455463b9a020d40ff8a00216` | pierde 1 renglón; llave corrompida | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2023_gf_ecd_epe.csv |
| `cuenta_publica_2024_gf_ecd_epe.csv` | 16:39 | 104,728,959 | `97fe8043a84801d19e3a26b50eba5b08233257f50a8f99bfe9184f89df328870` | pierde 3 renglones; +9,699 MDP en el ramo 51 | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/CSV/cuenta_publica_2024_gf_ecd_epe.csv |
| `cuenta_publica_2025_gf_ecd_epe.xlsx` | 16:54 | 29,110,060 | `6330b2a06376d8482485ce57f89a4db12faf99a49418d04403807036b20b4c3d` | ninguno: idéntico al CSV | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2025_gf_ecd_epe_xlsx.zip (extraído del zip) |

## 3. Documentación de la fuente

Vienen dentro del zip del xlsx de 2025, junto con el propio conjunto de datos. Los ejercicios 2020 a 2024 se descargaron como archivos sueltos, sin diccionario ni metadatos.

Para los tres archivos extraídos de ese zip (este par y el xlsx de 2025 de la sección 2), la huella registrada corresponde al archivo **extraído**, no al zip: para verificarlos hay que descomprimir primero y calcular la huella de cada archivo.

El diccionario no corresponde exactamente a ninguno de los dos archivos que acompaña: documenta la columna como `RAMO`, mientras el xlsx la nombra `R` y el CSV usa una nomenclatura distinta en todas sus columnas.

| Archivo | Hora | Bytes | SHA-256 | URL de origen |
|---|---|---:|---|---|
| `Diccionario_de_Datos_Cuenta_Pública_2025.csv` | 16:44 | 6,527 | `e6832d37746b8216b87befd983f0c7b1c56c50a1e78c7a86fdfc32d354426b9c` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2025_gf_ecd_epe_xlsx.zip (extraído del zip) |
| `Metadatos_Cuenta_Pública_2025.xls` | 16:44 | 26,112 | `dbe1d242467ecbb24e897b8f92dd89c4ed0a823503447101df6fa9ad12b6c950` | https://www.transparenciapresupuestaria.gob.mx/work/models/PTP/DatosAbiertos/BD_Cuenta_Publica/XLSX/cuenta_publica_2025_gf_ecd_epe_xlsx.zip (extraído del zip) |

## 4. Verificación contra el informe oficial

Cuenta Pública 2024, Tomo VII Sector Paraestatal, ramo 51 GYN (Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado), Información Presupuestaria.

Ambos documentos reportan un devengado total de **480,321,127,620 pesos**. Coincide con el xlsx de datos abiertos (480,321.1 MDP) y no con el CSV (490,020.4 MDP). Es el fundamento de la decisión de cargar desde xlsx.

Ruta de navegación: `cuentapublica.hacienda.gob.mx` → 2024 → Tomo VII → buscar "TRABAJADORES DEL ESTADO" → 51 GYN → Información Presupuestaria.

| Archivo | Hora | Bytes | SHA-256 | URL de origen |
|---|---|---:|---|---|
| `Verificacion/51GYN.03.F_ECONO.xls` | 17:35 | 7,168 | `92256c67d9a6924a053a6776073e9fb12e4ee9aaeafe07607c8e1d37d7fe479a` | https://www.cuentapublica.hacienda.gob.mx/work/models/CP/2024/tomo/VII/51GYN.03.F_ECONO.xls |
| `Verificacion/51GYN.03.F_OBJGASTO.xls` | 17:35 | 15,872 | `7ec819618a3ffa3a320f835df6f99afb0baf68a5e3effc2b4f2a3a3f09ed9c95` | https://www.cuentapublica.hacienda.gob.mx/work/models/CP/2024/tomo/VII/51GYN.03.F_OBJGASTO.xls |

Copia archivada en el Wayback Machine el 18 de septiembre de 2026, 16:22:17 UTC:

- `51GYN.03.F_OBJGASTO.xls`: https://web.archive.org/web/20260918162217/https://www.cuentapublica.hacienda.gob.mx/work/models/CP/2024/tomo/VII/51GYN.03.F_OBJGASTO.xls

La copia archivada es idéntica byte por byte a la local, comprobado con dos algoritmos independientes: SHA-256 sobre el contenido original de la captura (`7ec81961...`, 15,872 bytes) y SHA-1 en base32 registrado por el propio índice del Wayback (`QUHEYL6HC5IP45VEIWG6QGI2AM4PFADX`). Este documento por sí solo reporta el devengado total de 480,321,127,620 pesos, suficiente para sustentar la decisión de carga.

El intento de archivar `51GYN.03.F_ECONO.xls` (16:13:27 UTC) no produjo captura: no aparece en el índice del Wayback, aunque la de `F_OBJGASTO`, nueve minutos posterior, sí. Queda como pendiente.

### Clasificador por Objeto del Gasto (CONAC)

Fuente de la tabla `presupuesto.dim_capitulo`. Esa tabla no viene en los datos publicados: la agrega el proyecto para que el capítulo de gasto sea consultable (ver `src/sql/02_semantica.sql`). Los nueve capítulos se verificaron contra este documento, cuyo encabezado declara "Última reforma publicada DOF 22-12-2014".

Página de origen: normatividad vigente del CONAC (`https://www.conac.gob.mx/es/CONAC/Normatividad_Vigente`), inciso f). Historia en el Diario Oficial de la Federación: emisión el 9 de diciembre de 2009; reformas el 10 de junio de 2010, el 19 de noviembre de 2010 y el 22 de diciembre de 2014. Esta última es la más reciente que lista la página del CONAC al 18 de septiembre de 2026.

| Archivo | Obtenido | Bytes | SHA-256 | URL de origen |
|---|---|---:|---|---|
| `Verificacion/NOR_01_02_006.pdf` | 18 sep. 2026, 10:12 | 438,478 | `3c178cf222dd18744f3333840065f1d1b4df40d0f65aa3e564488c7265741d56` | https://www.conac.gob.mx/work/models/CONAC/normatividad/NOR_01_02_006.pdf |

## 5. Consultas documentadas sin archivo

Observaciones hechas en portales el 17 de septiembre de 2026 que sustentan decisiones del proyecto pero no produjeron un archivo. Al ser páginas que pueden cambiar, conviene archivarlas en `web.archive.org` y citar la copia archivada.

| Portal | Observación | Consecuencia |
|---|---|---|
| Datos abiertos del Gobierno de Tamaulipas, categoría Finanzas: `tamaulipas.gob.mx/datosabiertos/categorias/finanzas/` | El 17 de septiembre de 2026, cuatro conjuntos: tres de recaudación predial municipal de 2019 y un listado de normatividad; ninguno de presupuesto estatal; última modificación, junio de 2021. La copia del Wayback Machine del 17 de junio de 2024 muestra **diez** conjuntos en la misma categoría, entre ellos "Información financiera del Gobierno del Estado de Tamaulipas" (publicado en enero de 2024) e "Información financiera del presupuesto asignado de la Secretaría de Finanzas" (mayo de 2021). Seis de los diez se retiraron entre ambas fechas, incluidos los dos de contenido presupuestario. Copia archivada: https://web.archive.org/web/20240617164459/https://www.tamaulipas.gob.mx/datosabiertos/categorias/finanzas/ | La ruta estructurada es federal; Tamaulipas aporta la ruta documental. La disponibilidad de datos abiertos estatales no es estable: conjuntos publicados se retiran sin aviso, y sin archivo de terceros no quedaría evidencia de que existieron. |
| Plataforma Nacional de Transparencia, consulta pública: `consultapublicamx.plataformadetransparencia.org.mx` | Verificación anti-bot que entra en bucle en navegador automatizado; desde un navegador convencional es accesible (comprobado el 18 de septiembre). La sección de datos abiertos cubre solo solicitudes y quejas, no obligaciones de transparencia. | Sin descarga masiva de los formatos de transparencia: se consultan uno por uno. |
| Lineamientos Técnicos Generales 2026, artículo 65 fracción XIX | El formato de presupuesto desglosa solo por capítulo de gasto; las demás clasificaciones se publican como hipervínculo a documento. | Los formatos de transparencia no sirven como fuente de la ruta estructurada. |

## Pendientes

- Reintentar el archivado de `51GYN.03.F_ECONO.xls` (sección 4). No es crítico: `F_OBJGASTO`, ya archivado y verificado, reporta la misma cifra. Para comprobar una captura nueva, consultar el índice: `https://web.archive.org/cdx/search/cdx?url=cuentapublica.hacienda.gob.mx/work/models/CP/2024/tomo/VII/51GYN.03.F_ECONO.xls&fl=timestamp,statuscode,digest` y comparar el `digest` con `BBTP7I3NQAWICQZCK3RBYSGIPPPRZ2C3`, que es la huella SHA-1 en base32 de la copia local.
- Archivar el estado actual de la página de Tamaulipas: el primer intento, el 18 de septiembre, devolvió error 504 del servidor de origen. Sin esa copia, los cuatro conjuntos actuales descansan solo en la observación propia, mientras que los diez de 2024 ya tienen copia de terceros.