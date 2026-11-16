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
