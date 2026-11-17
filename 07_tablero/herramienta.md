# Herramienta de acopio y tablero

Alternativa local: LibreOffice Calc (formato ODS, LibreOffice bajo MPL 2.0 y licencias complementarias) junto con una vista HTML local que lee el mismo conjunto de CSV/JSON y muestra filtros por corte, área y responsable. Grist Desktop no estaba disponible como ejecutable en el entorno de preparación. No se contabilizó una revisión cronometrada de 20 min ni una instalación fallida de 30 min. Se usa Calc como alternativa operativa.

**En Calc.** La conversión y la reapertura usaron LibreOfficeDev 26.8.0.0.alpha0. El archivo PANVIZ_Evaluacion.ods agrupa Criterios, Evidencias, Pruebas, Hallazgos, Acciones, Trazabilidad y los cortes Antes/Después. Las fórmulas recalculan los indicadores usando los registros. El campo con_evidencia se alimenta de la validación de rutas del generador. Las capturas incluidas son renderizaciones de las dos hojas del tablero. La validación del archivo ODS se hace al abrir/convertir con LibreOffice.

**En el tablero local.** Desde /evaluacion seleccionar corte, área y responsable. El indicador conserva el denominador del corte y los filtros ajustan criterios, barras y debilidades. Los IDs E abren el registro y la ruta relativa dentro del paquete. Los CSV se exportan con UTF-8 BOM para facilitar el uso en Calc.

**Acopio.** El formulario local exige criterio, descripción, ruta/enlace y autor. Guarda el borrador por navegador y exporta un CSV. El responsable propuesto consolida esos CSV, valida origen y duplicados y actualiza el índice. Limitación: este formulario no es multiusuario y requiere consolidación explícita. Para importación manual en Calc, abrir un CSV de exportaciones con codificación UTF-8 y separador coma.

**Verificación de preparación.** Se ejecutaron los casos técnicos del API local, el generador de CSV/JSON y la conversión a ODS. Las comprobaciones de navegador reportadas por el equipo se detallan abajo.


## Comprobaciones de acopio y exportación

**Fecha:** 15/11/2026. **Hora de creación del registro exportado:** 21:58 (Lima).
**Entorno documentado:** [LibreOffice 26.8.2.2 en Windows 11](../06_evidencias/herramienta/version_libreoffice.png).

| Comprobación | Resultado | Respaldo |
|---|---|---|
| Exportar un aporte | El formulario exportó una fila de prueba para C22 con descripción, referencia a E35, autor y fecha. | [CSV de prueba](../06_evidencias/herramienta/aportes_prueba.csv). |
| Importar el CSV | La hoja de la captura inicial mostró el texto en una sola columna. En una comprobación aparte se reimportó el mismo archivo en Calc con UTF-8, coma y comillas dobles como delimitador de texto. Se obtuvieron cinco columnas y una fila completa. | El mismo CSV permite repetir la comprobación. |
| Cambiar de corte | Las capturas muestran v1 y v2 con sus indicadores respectivos. En v2 aparecen 23 de 24 criterios con respaldo, 22 evidenciados y 12 de 12 pruebas aprobadas. | [Tablero v1](../06_evidencias/herramienta/tablero_v1.png) y [tablero v2](../06_evidencias/herramienta/tablero_v2.png). |

## Comprobación interactiva complementaria

**Fuente:** resultados reportados por Cielo Meza el 15/11/2026.

| Comprobación | Resultado reportado |
|---|---|
| Persistencia después de F5 | El contador de Acopio de aportes conservó el aporte de prueba tras recargar la página. |
| Filtro de área | En v2, VAL mostró solo los criterios de esa área. Al volver a Todas se restableció la vista. |
| Filtro de responsable | E4 mostró sus criterios. Los indicadores generales conservaron los totales de v2. |
| Apertura de E36 | El enlace de T09 abrió la [captura de P026 corregido a Chivay](../06_evidencias/pruebas_usuario/captura_T09_italo.png), con 25 aceptados y 5 rechazados. |

**Duración:** la sesión anterior no se cronometró. El valor de 7 min 20 s se reportó como simulado y queda excluido de la medición. La revisión cronometrada de 20 minutos sigue sin acreditarse.

## Actualizar las hojas de datos

El tablero HTML se actualiza ejecutando generar.py. Para sincronizar el ODS, abrir cada CSV como hoja aparte, seleccionar la codificación UTF-8 y copiar las columnas por nombre a la hoja que corresponda conservando su orden. En Criterios, mantener con_evidencia en la última columna: 1 para una lista con evidencia enlazada y 0 para una lista vacía. Las fórmulas de los dos paneles se refieren al intervalo de filas del corte. Si se agrega una fila a Hallazgos, extender el intervalo de esa hoja en las fórmulas de ambos cortes. Guardar una nueva copia ODS y actualizar las dos capturas si cambia el corte.

<!-- PANVIZ_COMPROBACIONES_20261117 -->
## Comprobaciones respaldadas con capturas del 17/11/2026

**Responsable de la comprobación:** Cielo Meza. Se incorporan capturas suministradas por ella de la sesión actual. Estas comprobaciones documentan funciones concretas; no acreditan una revisión cronometrada de 20 minutos ni una instalación de Grist de más de 30 minutos.

| Comprobación | Resultado visible | Respaldo |
|---|---|---|
| Importación de criterios | El archivo aparece separado en columnas: corte, ID, área, descripción, responsable, estado y justificación. Cielo reportó su apertura en LibreOffice. | [E39: criterios importados](../06_evidencias/herramienta/2026-11-17_importacion_criterios.png) |
| Exportación de aportes y apertura en hoja de cálculo | Se observan cinco columnas (criterio, descripción, referencia, autor y fecha) y dos registros. El nuevo aporte describe la prueba del formulario y la exportación CSV. La captura acredita el contenido exportado y su separación en columnas. | [E40: aportes exportados](../06_evidencias/herramienta/2026-11-17_aportes_columnas.png) |
| Filtro por responsable | El control muestra E4. Los indicadores generales conservan los valores de todo v2: 23/24 con evidencia, 22/24 evidenciados, 12/12 ejecutadas, 12/12 aprobadas y cero debilidades abiertas. La captura no incluye la matriz filtrada. | [E41: filtro E4 e indicadores](../06_evidencias/herramienta/2026-11-17_filtro_responsable.png) |
| Acceso a evidencia | La ficha E36 abre la imagen de T09, donde P026 está corregido y el resultado es 25 aceptados y 5 rechazados. Se comprobó el acceso y el contenido visible; esto no constituye una nueva medición de T09. | [E42: apertura de E36](../06_evidencias/herramienta/2026-11-17_apertura_e36.png) |

**Estado de estas comprobaciones:** documentadas con las capturas adjuntas. La persistencia tras F5 y el filtro VAL conservan el alcance de los resultados reportados anteriormente: estas imágenes no aportan una nueva captura de esas dos comprobaciones.

**Duración de la sesión actual:** no registrada. La revisión cronometrada de 20 minutos sigue sin acreditarse. Se mantiene la limitación de acopio local por navegador y consolidación manual mediante CSV.

**Versiones:** el generador recalcula las huellas de las interfaces vigentes y de los nuevos archivos al incorporar esta evidencia. Las capturas de pruebas anteriores conservan su fecha y versión originales.


## Declaración posterior de duración de la revisión

**Fuente:** datos comunicados por Cielo Meza en la conversación de preparación de la entrega.

| Campo | Valor declarado |
|---|---|
| Fecha de la revisión indicada por Cielo | 15/11/2026 |
| Inicio indicado | 22:07, hora de Lima |
| Fin indicado | 22:31, hora de Lima |
| Duración calculada entre las horas indicadas | 24 minutos |
| Persistencia tras F5 | Cielo indica que el aporte permaneció registrado. |
| Filtro VAL | Cielo indica que mostró solo los cuatro criterios de VAL. |

**Alcance del registro:** se conserva la declaración de la responsable. No se dispone de un registro contemporáneo del cronómetro que permita verificar las horas de inicio y fin. Este apartado no certifica una medición independiente.

**Distinción de fechas:** E39–E42 corresponden a las capturas aportadas el 17/11/2026. Respaldan las funciones visibles en ellas y no demuestran que esas capturas se tomaran durante el intervalo declarado del 15/11/2026. Se conservan sus fechas y nombres originales.

La justificación de Calc como alternativa a Grist se mantiene separada: no se afirma que una instalación haya superado 30 minutos.
<!-- /PANVIZ_COMPROBACIONES_20261117 -->

<!-- PANVIZ_GRIST_DURACION_REPORTADA -->
## Actualización de la incidencia de Grist

Cielo precisa que el intento de instalación duró **42 minutos hasta abandonar el intento**, durante un viaje con conexión lenta. Es una duración reportada retrospectivamente por la responsable; no se adjunta un log contemporáneo que la mida de forma independiente. Este dato completa la duración antes no registrada en la descripción de la contingencia.

Este intervalo corresponde al intento de instalar Grist. Es distinto de los 24 minutos declarados para la revisión funcional de Calc y del tablero. La alternativa operativa se conserva.
<!-- /PANVIZ_GRIST_DURACION_REPORTADA -->
